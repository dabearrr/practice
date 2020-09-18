# Ticketmaster
## Online movie ticket booking system
* Allows customers to buy theater seats online
* Customers can browse through movies currently being played and book seats

## Requirements and Goals of the System
* Functional Requirements
  * ticket booking service should be able to list different cities where its affiliate cinemas are located
  * once the user selects the city, the service should display movies released in that city
  * once the user selects a movie, the service should display the cinemas running that movie and its available show times
  * user should be able to choose a show at a particular cinema and book their tickets
  * service should be able to show the user the seating arrangement of the cinema hall
    * user should be able to select multiple seats according to their preference
  * user should be able to distinguish available seats from booked ones
  * users should be able to put a hold on the seats for for five minutes before they make a payment to finalize the booking
  * user should be able to wait if there is a chance that the seats might become available, when holds by other users expire
  * waiting customers should be serviced in a fair, fist come first serve manner
* Non functional Requirements
  * system would need to be highly concurrent
    * there will be multiple booking requests for the same seat at any particular point in time
    * service should handle this gracefully and fairly
  * core thing of the service is ticket booking
    * means financial transactions
    * ACID compliant, secure system

## Some Design Considerations
* assume no user authentication
* system will not handle partial ticket orders
  * user gets all requested seats or none
* fairness is mandatory
* to stop system abuse, restrict users to ten tickets at a time
* assume traffic would spike on popular releases and seats would fill fast
  * system should be scalable and highly available to handle these surges

## Capacity Estimation
* traffic estimates
  * assume 3 billion page views / mo, 10 million ticket sales / mo
* storage estimates
  * assume we have 500 cities and each city has 10 cinemas on average
  * there are 2000 seats in each cinema and two shows per day
  * assume each seat booking needs 50 bytes
    * IDs, number of seats, show_id, movie_id, seat_numbers, seat_status, timestamp
    * 500 cities * 10 cinemas * 2000 seats * 2 shows * (50 + 50) bytes = 2GB / day
  * 5 * 365 * 2GB = 3.6 TB of storage

## System APIs
* REST or SOAP APis exposed
* apis
  * search_movies
    * inputs:
      * api_dev_key
        * throttle callers
      * keyword
        * keyword to search on
      * city
        * city to filter movies by
      * lat_long
        * lat and long to filter by
      * radius
        * radius of the area in which we want to search for events
      * start_datetime
        * filter movies with a starting datetime
      * end_datetime
        * filter movies with a ending datetime
      * postal_code
        * filter movies by postal_code / zipcode
      * include_spellcheck
        * yes, to include spell check suggestions in the response
      * results_per_page
        * number of results to return per page
      * sorting_order
        * sorting order of the search result
    * output
      * json
        * list of movies and show times
  * reserve_seats
    * inputs
      * api_dev_key
      * seats_to_reserve
        * list of seats to reserve
      * session_id
        * users session id to track this reservation
        * once the reservation time expires, the user's reservation on the server will be removed using this id
      * movie_id
        * movie to reserve
      * show_id
        * show to reserve
    * output
      * JSON
        * returns status of reservation
          * success
          * reservation failed -- show full
          * reservation failed -- retry as users are holding lock

## Database Design
* data info
  * city can have multiple cinemas
  * each cinema will have multiple halls
  * each movie will have many shows and each show will have multiple bookings
  * a user can have multiple bookings
* schemas
  * movies
    * movie id
    * title
    * desc
    * duration
    * lang
    * release date
    * country
    * genre
  * shows
    * show_id
    * date
    * start_time
    * end_time
    * cinema_hall_id
    * movie_id
  * cinemas
    * cinema_id
    * name
    * total_cinema_halls
    * city_id
  * cities
    * city_id
    * name
    * state
    * zip code
  * cinema_halls
    * cinema_hall_id
    * name
    * total_seats
    * cinema_id
  * cinema_seat
    * cinema_seat_id
    * seat_number
    * type
    * cinema_hall_id
  * bookings
    * booking_id
    * number_of_seats
    * timestamp
    * status
    * user_id
    * show_id
  * show_seats
    * show_seat_id
    * status
    * price
    * cinema_seat_id
    * show_id
    * booking_id
  * users
    * user_id
    * name
    * password
    * email
    * phone
  * payments
    * payment_id
    * amount
    * timestamp
    * discount_coupon_id
    * remote_transaction_id
    * payment_method
    * booking_id
## High Level Design
* web servers manage user sessions
* app servers handle all the ticket management, storing data in the databases, interacting with cache servers for reservations

## detailed component design
* ticket booking workflow
  * user searches for movie
  * user selects movie
  * user is shown the available showings of the movie
  * user selects a showing
  * user selects the number of seats to be reserved
  * if required number of seats are available, user is shown a map of the theater to select seats
    * if so
      * once the user selects the seats, system will try to reserve those seats
    * if not
      * show is full, the user is shown the error message
      * the seats the user wants to reserve are no longer available, but other seats are available, so the user is taken back to the theater map to pick new seats
      * There are no seats available to reserve, but the seats are not booked yet
        * user is taken to the waiting page to wait for seats to either be booked or dropped
          * if seats become available, the user is taken back to the theater map page to choose seats
          * if all seats get booked are there are fewer seats in the reservation pool than needed, the user is shown the error message
          * user cancels the waiting, returns to movie search page
          * at max, a user can wait one hour, after that the user's session expires, taken back to movie search page
  * if seats are reserved successfully, the user has five minutes to pay
    * after payment, the seats are booked
    * if user does not pay in time, seats are freed from reservation pool

* How would the server track active reservations that are not booked? How would the server track the waiting customers?
  * need two daemon servers, one to keep track of all active reservations and remove any expired reservations
    * ActiveReservationService
  * other service keeps track of waiting user requests, as soon as enough seats are available, it notifies the longest waiting user
    * WaitingUserService

* Active Reservation Service
  * keep all reservations of a show in a data structure like LinkedHashMap or TreeMap
  * need fast indexing to remove reservations quickly once booking is complete
  * need to delete expired entries, linkedhashmap will allow us to see oldest items to delete them fast
  * key = show_id, value has booking_id and creation timestamp
  * reservation stored in Booking table, with expiry time
  * status marked as reserved
  * once booking is complete, status is marked as Booked and the reservation is removed from the reservation table
  * when reservaqtions expire we can remove it from booking table or marked as Expired
  * ActiveReservationService also works with financial systems to process payments
  * Whenever booking is completed or reservation expires, WaitingUsersService is signaled to update the customers
* Waiting Users Service
  * keep waiting users in a linkedhashmap
  * need quick indexing to remove users when they cancel their wait request
  * to serve users in first come first serve manner, the head of the ll points to longest waiting user, can also easily traverse if needed
  * hash table stores waiting users for every show
  * key is show_id, value is user_id, wait start time
  * Reservation Expiration
    * ActiveReservationsService keeps track of expiry of active reservations
    * client will be shown timer of expiration
    * to keep sync of timer, we can add a five second buffer on server to safeguard from a broken experience
      * client should never time out after the server, prevents successful purchase after time out

## Concurrency
* How to handle concurrency, s.t. no two users are able to book the same seat
  * we can use transactions in SQL databases to avoid any clashses
  * we can use transaction isolation levels to lock rows before update
  * ```
    SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
 
    BEGIN TRANSACTION;
     
    -- Suppose we intend to reserve three seats (IDs: 54, 55, 56) for ShowID=99 
    Select * From Show_Seat where ShowID=99 && ShowSeatID in (54, 55, 56) && Status=0 -- free 
 
    -- if the number of rows returned by the above statement is three, we can update to 
    -- return success otherwise return failure to the user.
    update Show_Seat ...
    update Booking ...
 
    COMMIT TRANSACTION;  
    ```
  * Serializable is the highest isolation level
  * guarantees safety from dirty, nonrepeatable, and phantom reads
  * within a transaction, if we read rows, we get a write lock on them so that they cant be updated inbetween the read and write
  * once the transaction is complete, we can track the reservation in active reservation service

## Fault Tolerance
* What happens when Active Reservation Service or Waiting Users Service crashes?
  * whenever active reservation service crashes we can read all active transactions from the Booking table
    * reservations are marked as status reserved
  * we can also have leader-follower config, follower handles failover

## Data partitioning
* Database partitioning
  * partition by movie_id
    * all shows of a movie on same server, bad for hot movies
  * better: partition by show_id
    * even load distribution
* active reservation service and waiting user service partitioning
  * web servers manage all active users' sessions and handle communication with the users
  * consistent hashing allocate application servers for both active reservation service and waiting user service
    * based on show_id
    * all reservations and waiting users of a particular show will be handled by a certain set of servers
    * for Load Balancing, our consistent hashing server allocates 3 servers per show
    * whenever a reservation expires:
      * update db to remove booking, update seats' status in show_seats table
      * notify user that their reservation expired
      * broadcast message to all waiting users service servers that are holding users of that show
        * the longest waiting user needs to be found
        * consistent hashing tells us which servers to check
      * send a message to the waiting users service holding the longest waiting user to process their request if required seats have become available
* Whenever a reservation succeeds
  *  the server holding that reservation sends a message to all servers holding the waiting users of that show, so that those servers can expire waiting users that need more seats than the available seats
  *  upon received the message, servers holding waiting users query the db to find how many free seats remain.
     *  can use cache here
  *  expire all waiting users who want to reserve more seats than the available seats
     *  for this, waiting user service must iterate through the linked hash map of all the waiting users
     * 
