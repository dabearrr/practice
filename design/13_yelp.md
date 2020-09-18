# Yelp

## Why Yelp or Proximity Server
* used to discover nearby attractions

## Requirements and Goals of the System
* goals
  * store information about different places so that users can perform a search on them
  * upon query, our service returns a list of places around the user
* functional requirements
  *  users should be able to add delete update places
  *  given their location (long/lat) user should be able to find all nearby places within a given radius
  *  users should be able to add feedback / review about a place
  *  feedback can have pictures, text, and a rating
*  non-functional requirements
   * users should have a real time search experience with min latency
   * our service should support a heavy search load

## Scale Estimation
* 500M place
* 100K queries per second
* 20% growth in places and QPS each year

## 4 Database Schema
* Each place has
  * location_id  8 bytes (2^(8*8)) = 2^64 space = 32 billion+
  * name (256 bytes)
  * latitude (8 bytes)
  * longitude (8 bytes)
  * description (512 bytes)
  * Category (1byte) (restaurant, coffee shop, theater)
* four byte number can uniquely identify 500m places, but we will use 8 bytes for future expansion
* total size: 793 bytes per place
* need to also store reviews, photos, and ratings of a place
* separate table for reviews
  * location_id 8 bytes
  * review_id 4 bytes: unique id of a review
  * review_text 512 bytes
  * rating 1 byte how many stars
* similarly, separate table for photos and reviews

## 5 System Apis
* search(api_dev_key, search_terms, user_location, radius_filter, maximum_results_to_return, category_filter, sort, page_token)
  * api_dev_key string
    * api dev key of a registered account
    * used to throttle
  * search terms string
    * string containing search terms
  * user location string
    * location of the user performing the search
  * radius filter int
    * optional search radius in meters
  * maximum results to return int
  * category_filter string
    * optional category to filter search results
  * sort number
    * optional sort mode (0 - default, 1 - distance, 2 highest rated)
  * page_token string
    * token specifies a page in the result set to return
  * returns JSON of resulting places matching the search query

## 6 Basic system design and alg
* we need to store and index each dataset above
* indexing should be read efficient
  * searching is expected to be real time
* given that the location of a place doesnt change often we dont have to worry about frequent updates of the data
* SQL solution
  * store all data in a sql db
  * each place is a row, identified by location_id
    * long, lat in columns
      * have index on both fields
  * query for places nearby x, y
    * ```Select * from Places where Latitude between X-D and X+D and Longitude between Y-D and Y+D```
  * how efficient is this?
    * each index can return a huge list
    * finding intersection is slow
    * we need to shorten these lists
* Grids
  * we can divide the map into smaller grids
  * each grids stores places residing within a certain range of long, lat
  * based on a given location and radius, we can find all neighboring grids and query these to find nearby places
  * grid_id (4 bytes) uniquely ids grids
  * in the db we attach a grid_id to every location
  * now the query is:
    * ```Select * from Places where Latitude between X-D and X+D and Longitude between Y-D and Y+D and GridID in (GridID, GridID1, GridID2, ..., GridID8)```
  * Should we keep our index in mem
    * maintaining the index in mem will improve performance
    * we can keep our index in a hash table where key is grid number and value is the list of places in that grid
  * how much mem to store the index?
    * assume 10 mile search radius
    * given the total area of earth is 200m sq miles
    * we will have 20 million grids
    * we need 4 bytes to unique identify a space of 20m
    * since location_id is 8 bytes, we need 4GB of memory
      * 20m * 4 bytes + 500m * 8 bytes = 4GB
    * this solution is still slow for grids that are densely populated
    * this problem can be solved with dynamically sized grids
* Dynamic Grids
  *  lets assume our max grid size is 500
     * to allow for faster search
  * whenever a grid reaches this limit, we break it into 4 equally sized grids and distribute places among them
  * This means dense places like San Francisco will have many grids and sparse places like the pacific Ocean will have large grids with places only around the coasts
  * What data structure can hold this info
    * A tree in which each node has four children
    * each node will represent a grid and contain info about all places in that grid
    * if a node reaches 500 places we break it down into 4 nodes and distribute places among them
    * all leaf nodes represent grids that cannot be further broken down
  * how do we build this QuadTree?
    * one node is the whole world
    * since it has more than 500 location, we break it down into 4 nodes and distribute locations among them
    * keep repeating this process until there are no nodes with > 500 locations
  * How will we find the grid for a given location?
    * start with root, search downwards to find our required node / grid
    * if node has child, go to child with given location
    * else we found our node
  * How will we find neighboring grids of a given grid?
    * Since only leaf nodes have a list of locations, we can connect leaves with a doubly linked list
    * another approach is using parent nodes
    * traverse the parent ptrs to search for adjacent nodes
    * once we have nearby location_ids, we can query the backend db for details on the places
  * search workflow
    * find the node with the user's location
      * if it has enough locations, return these
      * else get neighboring nodes until we find the required number of places or exhause our search based on maximum radius
  * how much memory for quadtree?
    * for each place, if we only cache the location_id and lat/long
      * needs 12GB
        * 24 bytes * 500m = 12GB
    * since each grid can have a max of 500 places, how many grids will we have
      * 500m locations
      * 1m grids
    * that is 1m leaf nodes
    * approx 1/3 internal nodes
    * each node will have 4 ptrs
    * 1m * 1/3 * 4 * 8 = 10MB
  * so the total memory will be 12.1 GB
  * how do we insert a new place?
    * insert to db
    * insert to quadtree
      * if our quadtree is distributed, we need to find the grid / server of the new place and store it there

## Data Partitioning
* what if we have a huge number of places s.t. our index does not fit in mem?
* 20% growth each year, we will reach the memory limit of the server in the future
* also, what if one server cannot serve the desired read traffic?
* we must distribute the quadtree
* Sharding based on regions
  * divide places into regions (like zip codes), s.t. all places belonging to a region will be stored on a fixed node
  * to store a place we will find the server through its region and similarly, while querying for nearby places we will ask the region server that contains user's location
  * issues
    * hot regions
      * if a region is hot, it would have a lot of queries, making it perform slow
    * over time some regions can store many more places compared to others
      * maintaining uniform distribution will be difficult
* Sharding based on location_id
  *  hash function maps location_id to a server where we will store the place
  *  while building the quadtree, we iterate through all the places and calculate the hash of each location_id to find the server which holds it
  *  to find places near a location, we have to query all servers, each server returns a set of nearby places
  *  centralized server aggregates the results
*  Will we have different quadtree structure on different partitions?
   * yes
     * it is not guaranteed we will have an equal number of places in any given grid on all partitions
     * all servers should have an approximately equal number of places
     * different tree structure should cause no issue

## Replication and Fault Tolerance
* Having replicas of QuadTree servers can provide an alternate to data partitioning
* to distribute read traffic, we just have replicas of each quad tree server
* we can havbe a leader - follower configuration where followers only serve read traffic, leader serves writes
* followers are eventually consistent with write server
* what happens when quad tree server dies
  * we can have a secondary replica of each server and if primary dies, follower can perform failover
  * leader and followers will have same tree structure
* what if both primary and secondary servers die at the same time
  * we have to allocate a new server and rebuild the same QuadTree on it
  * how do we know if we dont know which places were kept on it
  * brute force is to iterate through whole places db to get places that should be on there, filtering using hash function
  * how can we efficiently retrieve a mapping between places and quadtree server
    * we have to build a reverse index
    * we can have a separate quadtree server to hold this
    * build a hashmap where key is quadtree server number, value is a set of all the places on that server
    * need to store location id and lat long with each place
    * set will enable fast add / remove
    * whenever a quadtree needs to rebuild, it hits this reverse index to know which places it needs
    * we should also have replicas of this reverse index server for fault tolerance
    * if reverse index server dies, it can traverse through the whole db to rebuild it self

## Cache
* introduce cache in front of our db
* memcached
* app servers hit cache before db
* can adjust size of cache by user usage patterns
* LRU is good eviction policy

## Load Balancing
* LB layer at two places
  * clients to app servers
  * app servers to backend quad tree servers
* round robin is good to start
  * simple
  * handles dead servers by removing from rotation
  * bad at considering server load
  * can use more complex lb based on server load

## Ranking
* what if we want to rank places based on popularity instead, or relevance
* How can we return most popular places within a given radius
  * assume we track popularity
  * aggregated number can represent this (stars)
  * store this number in db and quadtree
  * while searching for the top 100 places in a radius, we can ask each partition to return the top 100 places with max popularity
  * aggregator server merges results, returns top 100 of these
  * we built this system assuming updates are not frequent
  * to update the popularity of a place in quadtree can be very slow if we do it on every rating left
  * we can do it few times a day instead, when load is low
