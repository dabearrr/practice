# Instagram

## Functional Requirements, non func reqs, extended reqs
### Functional requirements
* users can upload / download / view photos
* users can perform searches based photo / video titles
* users can follow other users
* The system should be able to generate and display a user's News Feed consisting of top photos from all the peopel the user follows

### Nonfunctional requirements* our service must be highly available
* < 200 ms latency for News Feed generation
* Consistency can take a hit, if a user doesnt see a photo for a while, it's ok
* highly reliable, dont lose uploaded photo / videos

no tags, no comments

## Some Design Considerations
* read heavy system
* want to fetch photos fast
* users can upload as many photos as they want
  * efficient management of storage is important
* low latency expected while viewing photos
* data should be 100% reliable

## Capacity estimation
* 500m total users, with 1m daily active users
* 2m new photos every day, 23 new photos / sec
* average photo size 200Kb
* 1 day of photos storage = 2m * 200kb = 400 GB
* 10 years storage:
  * 10 * 365 * 400 GB = ~1500TB

## High Level System Design
* support 2 scenarios, upload and view / search image
* object storage and metadata storage


## Database Schema
* need user data, photo data, and follower data
* photo data fetches all photo related info
  * it will need an index on photoId, creation date since we need to fetch recent photos first

* Photo table

  * key = photo_id
  * user_id
  * photo_path (reference to photo)
  * photo_latitude
  * photo_longitude
  * user_latitude
  * user_longitude
  * creation_Date

* User table

  * key = user_id
  * name
  * email
  * date_of_birth
  * creation_date
  * last_login

* UserFollow table

  * key = user_id_1, user_id_2

* Can use an RDBMS like MySQL / Postgres since we need joins
* We store photos in a distributed file storage like S3 or HDFS
* Can can also use NoSQL, since it scales very well
    * We need to store relationships between users and photos, to know who owns which photo
    * need to store list of people a user follows
    * we can use Cassandra (or any NoSQL store with wide column support)
      * wide column means key is key, value can have any amount of columns
        * means the schema is not strict
    * to store relations between users and photo, we have a denormalized UserPhoto table
    * same for UserFollow
    * key-value stores keep a number of replicas for reliability
    * deletes are lazy

## Data size estimation
* how much data in each table?
* 10 year storage
* User
  * assuming each int and datetime is 4 bytes, each row will be 68 bytes
  * uid 4b + Name 20b + email 32b + dob 4b + creation_date b + last_login 4b
  * with 500m users, that is 32GB of storage 500m * 68bytes
* Photo
  * each row will be 284b
    * pid 4b + uid 4b + photo_ref 256 bytes + photo_lat 4b + photo_long 4b + user_lat 4b + user_long 4b + creation_Date 4b
    * 2m new photos / day * 284bytes = 0.5GB / day => 1.88TB in 10 years
* UserFollow
  * assuming an average of 500 follows per user
  * row is 8 bytes (two ints)
    *  500m users * 500 followers * 8bytes = 1.82TB
*  32GB + 1.88 TB + 1.82TB ~= 3.7TB over 10 years


## Component Design
* photo uploads can be slow since they have to go to disk
* reads will be faster, especially if served from cache
* uploading users can consume all available connections, as uploading is slow
  * means reads cant be served if system is busy will all the writes
#### _keep in mind that web servers have a connection limit_
* if a web server has a limit of 500 concurrent connections, then it can't have more than 500 concurrent reads or uploads
* to handle this bottleneck, we can split reads and write into separate services
* we will have dedicated servers for reads and different servers for writes
  * ensures that uploads dont hog the system
  * allows us to scale and optimize each of these independently

## Reliability and Redundancy
* Losing files is not an option
* we will store copies of each file
* same principle applies to other components
* if we want high availability, we will need multiple replicas of services
  * so if a few services die, the system remains running
  * redundancy removes the single point of failure


## Data Sharding
* metadata sharding
* partitioning on user_id
  * keep all photos of a user on the same shard
  * Assume that we keep 10 shards
  * we find the shard number using user_id % 10 and store the data there
  * to uniquely indentify any photo in our system, we can append shard number to photo_id
  * how do we generate photo_ids
    * each db can have its own auto increment sequence for photo_ids
    * since we append shard_id with each photo_id it is unique
  * issues with this system
    * how do we handle hot users, many people follow these hot users and see their photos
    * some users will have a lot of photos compared to others, thus making a non-uniform distribution of storage
    * what if we cannot store all pictures of a user on one shard?
      * distributing photos of a user onto multiple shards may cause latency issues
    * storing all photos of a user on one shard can cause unavaility issues if that shard goes down
* partition based on photo_id
  * generate unique photo_ids, then find a shard through photo_id % 10, the above problems are solved
    * we wont need to append shard_id with photo_id as photo_id will be unique in the system
  * we cannot have an auto incrementing sequence in each shard to get photo_id since we need the photo_id first to find what shard to put it on
  * we could dedicate a separate database instance to generate auto-incrementing ids.
    * assuming our photo_id fits in 64 bits, we can define a table containing only 64 bit id field
    * whenever we add a photo to our system, we insert a new row in this table and get that id to be our photo_id
    * This key generating db would be a signel point of failure
    * as a workaround, we could have two such databases
      * one generates even ids, the other generates odd ids
      * we can put a load balancer in front of both of these dbs to robin robin between them and deal with downtime
      * the two dbs can be out of sync and cause NO issue
      * we can extend this system to define separate ID tables for Users, Photo-Comments or other objects in our system
  * alternatively, we can implement a key generation scheme similar to KGS from tinyurl
    * pregenerated keys table
  * how do we handle future growth
    * large number of logical partitions
      * in the beginning, multiple logical partitions preside on a single physical db
      * each db server can have multiple dbs on it
        * means we can have separate databases for each logical partition on any server
        * whenever we feel a particular db server has a lot of data, we can migrate some logical partitions from it
        * maintain a config file that maps logical partitions to db servers
          * enables us to move partitions easily, just update config


## Ranking and News Feed Generation
* we need to fetch to latest, most popular and relevant photos of the people the user follows
* lets assume we need the top 100 photos for a user's News Feed
  * Get list of people the user follows
  * Fetch metadata of top 100 photos each person has
  * submit all photos to ranking algorithm
  * return top 100 ranked
  * this approach would have high latency as we need to query many tables and perform sorting / merging / ranking on the results
  * to improve the efficiency we can pre-generate the News Feed and store it in another table
* _pregenerating the news feed_
  * we can have dedicated servers that are continuously generating users' new feeds and storing them in a UserNewsFeed table.
  * whenever a user needs the latest photos for their News Feed, we simply query this table and return the results to the user
  * When servers are generating NewsFeeds for users
    *  query the UserNewsFeed table to get the last time the news feed was generated for that user
    *  nnews feed data is generated from that time onwards
*  Approaches for sending News Feed contents to the users
   * Pull
     * clients pulls the new feed  contents from the server regularly or manually
     * issues
       * new data may not be shown until client pulls
       * most pulls will be empty response if there is no data
   * Push
     * servers push new data to the users
     * users maintain a Long Poll request with the server for receiving the updates
     * issues
       * a user who follows a lot of people / celebrity with many followers
         * in this case the server pushes updates very frequently
   * Hybrid
     * We can move all the users with a high number of follows to a pull model
     * push data to users who only have a few hundred or few thousand follows
     * Another approach:
       * push data to all users a certain limited frequency
         * letting users with a lot of follows / updates to regularly pull data
## News Feed Creation with Shard Data
* requirement for new feed is the fetch the latest photos from all people the user follows
* we need a machanism to sort photos on their craetion time
* to do this efficiently, we can make photo creation time part of the photo_id
* as we will have a primary index on photo_id, it will be quick to find the latest photo_ids
* we can use epoch time for this
* photo_id has two parts
  * epoch time
  * auto incrementing sequence
  * so we take epoch time and append a auto incrementing sequence to make the photo_id
  * to get the shard, we take photo_id % 10
* size of the photo_id?
  * How many bits to store the number of seconds for the next 50 years
    * 86400 sec / day * 365 * 50y => 1.6 billion secs
    * 31 bits
    * on average, we expect 23 photos per second
      * we can allocate 9 bits to store the auto incremented sequence
      * this sequence will reset every second

## Cache and Load balancing
* need a massive-scale photo delivery system to server global users
* We should push content closer to users using a large number of geographically distributed photo cache servers and use CDNs
* We can introduce a cache for metadata servers to cache hot database rows
  * Memcache to cache the data
  * application servers quickly check the cache before hitting db
  * LRU is a good cache eviction policy
* How can we build more intelligent cache
  * 80 - 20 rule (20 % of daily read volume for photos generates 80% of traffic)
  * we should cache the top 20% of DAILY read volume of photos and metadata
