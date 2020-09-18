# Twitter

## What is Twitter
* post 140 characters messages
* users post and read tweets
* unregistered users can only read

## requirements and goals
* functional
  * users can post new tweets
  * users can follow other users
  * users can favorite tweets
  * service can generate and display a user's timeline
    * has top tweets from followed users
  * tweets can contain photos and videos

* non functional
  * highly available
  * <= 200 ms latency for timeline generation
  * consistency can take a hit in the interest of availablity

* extended reqs
  * searching for tweets
  * replying to a tweet
  * trending topics
  * tagging other users
  * tweet notification
  * who to follow suggestions
  * moments

## capacity estimation and constraints
* one billion total users
* 200m daily active users
* 100m new tweets per day
* on average, each user follows 200 people
* favorites per day?
  * assume five favorites / day
  * 1 billion favorites / day
* total tweet views
  * user visits timeline 2x a day
  * visits five other people's pages
  * if a user see 20 tweets / page
    * 200m dau * ((2 + 5) * 20 tweets) = 28 billion tweet views / day

### storage estimates
* each tweet has 140 characters
* 2 bytes / char
* need 100m * (280 + 30) bytes = 30 GB / day
  * 55 TB over five years
* user data
  * assume we store user_id, user_name, email, last_login, creation_date
    * int, str, str, timestamp, date
    * assume this fits in 300 bytes
    * 300 bytes * 1 bil users = 300 GB
* follows
  * we will store user_id, follow_user_id
    * 64 bytes
    * 1 bil users * 200 follows * 64 bytes
      *  4 TB
*  favorites
   * user_id, tweet_id
     *  64 bytes
     *  64 bytes * 100m * 365 * 5y
        * 12 TB
* media
  * assume every fifth tweet has a photo and every tenth has a video
  * on average a photo is 200kb and a video is 2MB
  * 100m/5 * 200kb + 100m/10 * 2MB = 24TB / day

### Bandwidth Estimates
* total ingress is 24TB / day = 290MB / sec
* 28B tweet views /day
* egress:
  * 28B * 280 bytes of text / 86400s => 93MB/s
  * 28B/5 * 200kb / 86400s => 13GB/s
  * 28B / 10 / 3 * 2MB / 86400s => 22GB/s
* total ~= 35GB/s

## System APIs
* REST API or SOAP API to expose the service
* definition
  * tweet(api_dev_key, tweet_data, tweet_location, user_location, media_ids)
    * api_dev_key string
      * used to throttle api calls
    * tweet_data string
      * text of the tweet
    * tweet_location string
      * optional location long, lat
    * user_location str
      * optional location
    * media_ids (Arr)
      * list of media_ids to be associated with the tweet
        * video, photo refs
          * these are uploaded separately
  * returns string
    * successful post will return the URL to access the tweet
    * otherwise, http error

## High Level System Design
* need to efficiently store all the new tweets
  * 100m / 86400 => 1150 tweets / sec
  * 28B / 86400 = 325k tweet reads / sec
* read heavy system
* need application servers to serve all these requests, with load balancers in front of them to distribute traffic
* backend
  * need an efficient database to store all the new tweets and support many reads
  * need file storage for photos / videos
* traffic will be unevenly distributed
  * people use twitter during the day
  * expect spikes of up to few thousand writes /sec, 1m reads / sec

## Database Schema
* tweets
  * tweetid int pk
  * user_id int
  * content str
  * tweet_lat int
  * tweet_long int
  * user_lat int
  * user_long int
  * creation_date datetime
  * num_favorites int
* users
  * user_id int PK
  * name str
  * email str
  * date_of_birth datetime
  * creation_date datetime
  * last_login datetime
* user_follows
  * user_id_1 pk int
  * user_id_2 pk int
* favorite
  * tweet_id pk int
  * user_id int pk
  * creation_date datetime

## Data Sharding
* read heavy 28B reads / day, 100m new tweets / day as well
* need to distribute tweet data to read / write efficiently
* Sharding based on user_id
  * store all of the data of a user on one server
  * while storing, we pass the user_id to our hash function which will map the user to a db server
    * we will store the user's tweets, favorites, follows there
    * querying for tweets / follows / favorites of a user
      * ask our hash function where we can find user's data
  * issues
    * what if a user becomes hot
      * there could be a lot of queries on the server holding the user
        * high load will affect the service performance
    * users can end up storing a lot of tweets over time or having a lot of follows compared to others
      * maintaining a uniform distribution of grow user data can be difficult
    * to recover from these situations either we have to repartition or redistribute the data or use consistent hashing
* Sharding based on tweet_id
  * hash will map tweet_ids to random servers
  * to search for tweets, we query all servers
    * each server will return a set of tweets
    * central server aggregates results
  * timeline generation example
    * application server gets all user's follows
    * app server sends query to all db servers get tweets from these follows
    * each db server will find tweets for each user, sorted by recency, return the top tweets
    * app server merges all results and sorts them again to return the top results
  * this approach handles hot users, but in contrast with sharding by user_id we have to query all db partitions to find tweets of a user
    * can result in higher latencies
  * we can futher improve performance using a cache to store hot tweets
* sharding based on tweet creation time
  * can fetch top tweets quickly and only have to query a small set of servers
  * problem is traffic will not be distributed
    * while writing, all tweets go to same server
    * similarly, while reading, reads will all hit the recent servers more than old data servers
* Combined approach: tweet_id + creation time
  * if we don't store tweet creation time separately and use tweet_id to reflect that, we get benefits of both approaches
  * finding latest tweets will be fast
  * we must make each tweet_id universally unique and each tweet_id should contain timestamp as well
  * tweet_id
    * two parts, epoch time + auto incrementing sequence
    * new tweet_id = current epoch time + auto incrementing sequence
  * size of tweet_id
    * bits for 50 years of epoch time?
      * 86400 sec /day * 365 * 50 = 1.6 Billion
      * 31 bits for the epoch time
      * since we expect 1150 new tweets / second, we have 17 bits to store the auto incremented sequence
      * 48 bits total for tweet_id
      * every second we can store 130k new tweets (2^17)
      * reset the auto incrementing sequence every second
      * we can have two db servers to generate the auto incrementing sequence
        * one for evens one for odds
      * example:
        * current epoch is  1483228800
          * 1483228800 000001
          * 1483228800 000002
      * if we make our tweet_id 64 bits, we can store tweets for 100 years
  * in the above approach, we still have to query all the servers for timeline generation, but reads and writes will be much faster
    * since we don't have a secondary index on creation time, write latency is faster
    * while reading, we don't need to filter on creation_time because our p key has epoch time included

## Cache
* use cache for db servers to cache hot tweets and users
* memcached
* app server hits cache before db
* cache replacement policy
  * cache is full
  * want to replace a tweet with newer hotter tweet
  * LRU
* intelligent cache
  * 80-20 rule
  * 20% of tweets hold 80% of read traffic
  * certain tweets are so popular most people read them
  * we should cache 20% of daily read volume from each shard
* what if we cache latest data
  * our service can benefit from this approach
  * 80% of users see tweets from the past 3 days only
  * we can try to cache all of the tweets from the past three days
  * 100m new tweets / day or 30GB / day (without photos or vids)
    * less than 100GB to cache
    * can easily fit on one cache server
    * should be replicated across multiple cache servers to distribute load
    * lb in front of caches
    * during timeline generation
      * ask cache if it has all recent tweets for user x
      * return all the data from cache if so
      * else query backend
    * similarly we can cache the photos and vids this way (last 3 days)
* cache is like a hash table
* key is owner_id, value is a doubly linked list containing all the tweets for the user from the past 3 days
  * insert new tweets at the front, pop old tweets from the back

## Timeline generation
* similar to insta
* pregenerate them at a fixed rate
  * use previous pregenerated timeline + add new tweets

## replication and fault tolerance
* read heavy
* need multiple secondary db servers for each db partition
* secondary servers are read only
* writes go to primary, replicated to secondaries
* failover primaries to secondaries

## load balancing
* three points
  * clients to app servers
  * app servers to cache servers
  * app servers to db servers
* round robin is simple and solid
  * handles dead servers by ignoring them
  * does not consider load
* can use a lb strategy that considers load

## monitoring
* collect data to get system insights
* metrics
  * tweet throughput (tweets / day or per sec) what is the daily peak
  * timeline delivery stats
    * tweets per day read
  * average timeline refresh latency
* tells us if we need more replication, lb, caching

## extending reqs
* serving feeds
  * get all latest tweets from the followed users
  * merge / sort them by time
  * use pagination to fetch / show tweets
  * only fetch top N tweets from all the people someone follows
  * N depends on viewport (screen size)
  * cache next top tweets to speed up
  * or pregenerate the feed for efficiency
* retweets
  * we can store the id of the original tweet and not store any content on the retweet object
* trending topics
  * cache most frequently occuring hashtags or search queries in the last N seconds
  * keep updating these every M seconds
  * rank trending topics based on frequency of tweets / searches / retweets / likes
* who to follow, suggestions
  * improves user engagement
  * can suggest friends of followed users
  * go several levels down to find famous people for suggestions
  * give preference to users with lots of follows
  * can use ML to reshuffle / reprioritize
    * recently increased follows
    * common followers
    * common location / interests
  * moments
    * get top news for different websites for past 1 or 2 hours
    * figure out related tweets
      * prioritize and categorize them using ML
        * supervised or clustering
  * search
    * indexing, rank, retrieval
