# Uber

## What is Uber
* book drivers for taxi rides
* drivers use their own cars to drive customers around
* customers and drivers use app to communicate

## Requirements and Goals
* Two users
  *  drivers
  *  customers
*  drivers need to regularly notify the service about their current location and availability to pick passengers
*  passengers get to see all nearby available drivers
*  customer can request a ride
   * nearby drivers are notified that a customer is ready to get picked up
* once a driver and a custoemr accept a ride, they constantly see each other's currnt location until the trip finishes
* upon reaching the destination, the driver marks the journey complete to become available again for the next ride

## Capacity estimation
* assume we have 300m customers and 1m drivers with 1m daily active customers and 500k daily active drivers
* lets assume 1m daily rides
* assume all active drivers notify their current location every 3 seconds
* once a customer requests a ride, the system should contact drivers in real time

## Basic System Design and Algorithm
* we can adapt our yelp solution
* QuadTree was previously built to be rarely updated
* two issues with dynamic grids
  * all active drivers are reporting their locations every 3 seconds
      * need to update our data structures for that
      * to update driver location need to find the right grid based on driver's previous location
      * if new pos is not in previous grid, need to remove it from there and move it to the correct grid
      * if the new grid reaches the max limit of drivers we have to repartition it
  * need a quick mechanism to report current location of all nearby drivers to active customers in the area
    * when a ride is in progress, we need to notify of the driver and passenger of their location
* QuadTree is fast to find nearby drivers, but updates are not guaranteed to be fast
* How much memory we need for DriverLocationHT
  * driver_id, current location and old location need to be stored
  * 35 bytes to store this
    * 1 million drivers can be scoped in 3 byte id
    * old latitude 8 b
    * old long 8 b
    * new lat 8b
    * new long 8b
  * with 1 million drivers we need 35m bytes -> 35MB
* how much bandwidth will our service consume to receive location updates from all drivers
  * if get driver_d and their location, that's 3 + 8 + 8 = 19 bytes per driver
  * with 500k daily active drivers sending info every 3 seconds, that's 19 bytes * 500k = 9.5MB every 3 seconds
* Do we need to distribute DriverLocationHT onto multiple servers?
  *  bandwidth and mem requirements dont require this
  *  for scalability, performance, and fault tolerance concerns we should distribute it
  *  DL servers hold the distributed DriverLocationHT these servers do:
     *  As soon as the server receives an update for a driver's location, they will broadcast that information to all interested customers
     *  The server needs to notify the respective QuadTree server to refresh the driver's location
     *  As discussed above, this can happen every ten seconds
*  How can we efficiently broadcast the driver's location to customers:
   * use a push model
     * http long poll
     * dedicated notfication service broadcasts current location of all drivers to all interested customers
     * when a customer opens the Uber app on their phone they query the server to find neaby drivers
     * on the server side, before returning the list of drivers to the customer, we will subscribee the customer for all the updates from those drivers
     * we can maintain a list of customers (subscribers) interested in knowing the location of a driver
     * whenever we have an update in DriverLocationHT for that driver, we can broadcast the current location of the driver to all subscribed customers
     * This way, our system makes sure that we always show the driver's current position to the customer
* How much memory will we need to store all these subscriptions
  * 1m daily active customers, 500k daily active drivers
  * assume on average 5 customers subscribe to one driver
  * assume we store all this info in a hash table so that we can update it efficiently
  * need to store driver_ids and customer_ids to maintain the subscriptions
  * 3 bytes for driver_id, 8 bytes for customer_id
    * 3 + 8*5 = 43 bytes => 43 bytes * 500k = 21MB
* How much bandwidth will it take to broadcast the driver's location to customers
  * 5 * 500k => 2.5 million broadcasts
  * broadcast just has 3byte driver_id and 8 byte long and late = 19 bytes * 2.5 million = 47.5MB/s
* How can we efficiently implement notification service?
  * HTTP long polling or push notifications
* How will the new publishers / drivers get added for a current customer?
  * we said customers will be subscribed to nearby drivers based on a query on launch
  * what if a new driver enters the area
  * to add a new driver dynamically, we need to keep track of the area the customer is watching
    * this will make our solution complicated
    * instead of pushing this info, clients can pull it
* How can clients pull this information about nearby drivers?
  *  clients can send their current location and the server will find all nearby drivers from the QuadTree to return them to the client
  *  upon receiveing the info, clients maps update with new driver positions
  *  Clients can query every 5 seconds to limit the number of server round trips
  *  simpler than push model
*  Do we need to repartition a grid as soon as it reaches the maximum limit?
   * We can have a cushion to let each grid grow a bit bigger before we decide to partition it
   * grids can grow / shrink an extra 10% before repartitioning them
   * this should decrease the load on high traffic grids
* Request Ride Use Case
  *  customer puts a request for a ride
  *  one of the aggregator servers gets the request, asks QuadTree servers for nearby drivers
  *  aggregator server collcats all results and sorts them by rating
  *  aggregator server sends notfication to top X (3) drivers in the list, first to respond gets the customer ride
  *  if non respond, request the next 3 drivers from the list
  *  once a driver accepts, the customer is notified


## Fault Tolerance and replication
* what if a driver location server or notification server dies?
  * need replicas of these servers
  * primary server dies, secondaries perform failover
  * store data in persistent storage like SSDs, ensure that if both primaries and secondaries fail, we can recover

## Ranking
* rank search result by not only proximity but also popularity or relevance
* how can we return top rated drivers in a radius?
  * assume we track overall ratings of each drivers in our db and quadtree
  * aggregated number can represent this
  * while searching for the top 10 drivers in our radius, we can ask each partition of the quadtree to return the top 10 drivers with a maximum rating
  * aggregator server merges results and gets top 10 from there

## Advanced Issues
* how will we handle clients on slow / disconnecting networks
* what if a client gets disconnected when they are part of a ride? How will we handle billing in this scenario?
* how about if clients pull all the info, compared to servers always pushing it?
