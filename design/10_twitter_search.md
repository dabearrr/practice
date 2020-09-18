# Designing Twitter Search

## What is Twitter Search
* tweets consist of plain text
* design system to efficiently store and search over all tweets

## Requirements and Goals
* Assume twitter has 1.5 billion total users 800 million daily active users
* 400 million tweets per day
* average size of a tweet is 300 bytes
* 500m searches per day
* query will consist of multiple words combined with and/or

## Capacity Estimation and Constraints
* Storage Capacity
  * 400m new tweets per day
  * 300 bytes average tweet
  * 400m *300 bytes = 120GB per day
* Bandwidth (storage / sec)
  * 120GB / 24 hours/ 3600 sec ~= 1.38 MB/sec

## System APIs
* SOAP or REST api to expose service
* search function
  * search(api_dev_key, search_terms, maximum_results_to_return, sort, page_token)
    * api_dev_key string
      * used to throttle clients
    * search terms string
      * string containing search terms
    * maximum results to return int
      * page size
    * sort int
      * type of sort to use
        * 0 - latest first
        * 1 - best matched
        * 2 - most liked
    * page token string
      * token to specify which page to fetch
  * returns JSON
    * list of tweets matching search terms
      * with constraints passed as params
      * each tweet can have user_id, name, tweet_text, tweet_id, creation_time, number of likes, etc

## High Level Design
* store all tweets into a db
* have a search index to track which word appears in which tweet
* this index will help us quickly find tweets users are trying to search

## Detailed Component Design
* Need to store 120 GB of new data / day
* Need a good partitioning scheme, given the large amount of data
* 5 years
  * 120GB * 365 * 5 = 200TB over 5 y
  * 400m * 365 * 5 = 730 billion tweets over 5 y
* If we never want to be more than 80% full at any time, we'll need 1.25 * 200 = 250TB of total storage
* Assuming we want fault tolerance, we'll need duplicates of the data
  * brings us to 500TB for 1 level of replication
* Start with simple design
  * tweets go to MySQL db
    * table has two columns
    * tweet_id, text
    * partition on tweet_id
    * define a hash function to map a tweet_id to a storage server
* how can we create system-wide unique tweet_ids?
  * 400m new tweets a day
  * 730b / 5y
  * to generate a space to hold 730b values, we need 5 bytes
    * 2 ^ 32
  * Assume we have a service to generate unique tweet_ids whenever we need to store an object
    * use idea from designing twitter
      * tweet_id uses timestamp + auto incrementing sequence
        * timestamp is good for databases, since they often sort data by key
        * auto incrementing sequence is thread safe counter, resets on new timestamp value
          * should be long enough to store amount of requests expected per second
* what does the index look like?
  * tweet queries consist of words
  * estimate index size
    * index for all english words + famous nouns
      * 300k english words + 200k nouns = 500k words in the index
      * average length of word is 5 characters
        * each char is one byte
        * 500k words * 5 chars * 1 byte = 2.5MB
  * want to keep index in memory for all the tweet from only past 2 years
  * 730b tweets / 5 years
  * 292b tweets / 2 years
  * each tweet_id is 5 bytes
    * 292 billion tweets * 5 bytes per tweet_id = 1460GB
  * index is like a big distributed hash table
  * key is word
  * value is list of tweetIds of all those tweets which contain that word
  * assuming on average we have 40 words per tweet
    * assume we will not index prepositions and small words like 'the', 'an', 'and', etc.
    * this would bring us to around 15 words per tweet
    * each tweet id would be stored 15 times in our index
      * 15 * 1460Gb = 21TB
  * assuming a heigh-end server has 144GB of memory, we would need 152 such servers to hold our index
  * We can partition our data based on two criteria
    * Sharding based on words
      * hash based approach
        * iterate through all words of a tweet
        * hash each word to find the server where it would be indexed
        * to find all tweets containing a specific word we have to only query the server containing the word
        * issues
          * hot word
            * there will be a lot of queries on the server holding that word
            * bad for performance
          * some words can store a lot more tweet_ids than others
            * tricky to maintain a uniform distribution of words
          * to recover from these we would need to repartition our data or use consistent hashing
    * sharding based on the tweet object
      * pass tweet_id to our hash function to find the server and index all the words of the tweet on that server
      * while querying for a particular word, we have to query all servers
      * each server returns a set of tweet ids
      * need a centralized server to aggregate the results

## Fault tolerance
* What happens if index server dies
  * keep a secondary replica of each server
  * perform failover if primary dies
* what if primary and secondary servers both fail
  * allocate a new server, rebuild the same index on it
  * how do we rebuild the index
    * if sharding based on tweet_id
      * brute force
        * iterate through the whole database and filter tweet_ids using our hash function to figure out all the required tweets to store on this server
        * inefficient, during the rebuildinmg time we could not serve any query
* how can we efficiently retrieve a mapping between tweets and index server
  * we need to build a reverse index to map all the tweet_ids to their index server
  * index-builder server can hold this information
  * need to build a hash table where key is the index server number and the value is a hashset containing all the tweet_ids kept at that idnex server
  * keep all tweet_ids in a hash_set
    * allows for fast add / remove
  * now to rebuild an index server
    * index server asks the index builder server which tweets to store
    * fetch those tweets to build the index
* we should also have a replica of the index-builder server for fault tolerance

## Cache
* deals with hot tweets
* memcached stores all hot tweets in memory
* app servers, before hitting the backend database check cache for tweet first
* consider client usage patterns for identifying how many cache servers we need
* LRU cache

## Load Balancing
* between client and application
* application and backend
* simple round robin can be adopted
  * distributes requests evenly
  * simple to implement, no overhead
  * takes dead servers out of roto
  * does not consider server load
* can use more intelligent load balancing solution which queries backend servers for their load
  * adjusts traffic based on load

## Ranking
* social graph distance, popularity, relevance
* ranking alg can calculate a popularity number based on likes or other attrs
* store popularity with the index
* each partition sorts results based on popularity number before returning results
* aggregator combines results, returns top results




