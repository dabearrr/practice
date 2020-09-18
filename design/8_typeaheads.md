# Typeahead Suggestion

## Why
* Typeaheads allow users to search for known and frequently searched terms.
* As the user types into the search box, it tries to predict the query based on the characters input
* used more to guide the user than speed up queries

## requirements and goals
* Functional
  * As the user ypes their query, our service should suggest top 10 terms starting with whatever the user has typed
* Non-functional
  * The suggestions should appear in real-time. The user should be able to see the suggestions within 200ms.

## Basic System Design and Algorithm
* We have a lot of string
* need to store strings in a way that users can search with any prefix
* service suggests next terms that will match the prefix
* we need minimal latency
  * need a scheme that can efficiently store data for fast queries
  * cant use db
  * need our index in memory in a highly efficient data structure
* We can consider a Trie
* tree like data structure, each node stores and character in a sequential manner
* can merge nodes with only one branch to save storage space
* consider case sensitivity
* assume case insensitive for now
* How to find top suggestion?
  * now that we can find the matching terms, how do we rank them
  * store the count of searches terminated at each node
  * cat's t has x where x is the amount of searches it received
* Given a prefix, how long will it take to traverse its sub-tree:
  * given the data amount we need to index, expect a huge tree
  * traversing a sub-tree would take really long
  * need to improve efficiency, currently too slow
* Can we store top suggestions at each node?
  * This can speed up our searches, but will require A LOT of extra storage
  * we can store top 10 suggestions at each node
  * to save storage cost, store references to end nodes instead of words
  * To get the word we need to traverse back using the parent reference from the end node
  * We will also need to store the frequency with each reference to track top suggestions
* How do we build the Trie?
  * Bottom up
  * parent nodes recursively call all child nodes to calculate their top suggestions and their counts.
  * Parent nodes will combine top suggestions from all of their children to determine their top suggestions
* How to update the trie?
  * assuming 5 billion searches / day
  * 60k queries / sec
  * if we try to update our trie on every query, it'll be extremely resource intensive
    * may also hamper read requests
  * we can try updating our trie in batches
    * As new queries come in, we log them and track frequencies
    * we can log every query or do sampling and log every 1000th query
    * ex: if we dont want to show a term which is searched for less than 1000 times, it is safe to log every 1000th query
    * we can use a map-reduce job to process all of the logging data periodically every hour
    * these mr jobs will calculate frequencies of all searched terms in the past hour
    * we can then update our trie with this new data
    * take the current snapshot of the trie and update it with all the new terms and their frequencies
    * we should do this offline as we don't want our read queries to be blocked by update trie requests
      * two options
        * make a copy of the trie on each server to update it offline. once done we can switch to start using it and discard the old one
        * we can have a leader - follower config for each trie server. we can update follower while the leader serves traffic.
          * once the update completes, follower can be new leader, then we update old leader
    * how can we update the frequencies of typeahead suggestions
      * since we are storing frequencies of our typeahead suggestions with each node, we need to update them too
      * we can update only differences in frequencies rather than recounting all search terms from scratch
      * if we're keep a sliding window of terms searched in last 10 days
        * we'll need to subtract the counts from the time period no longer included and add counts for the new time period being included
        * We can add and subtract using Exponential Moving Average of each term
          * EMA gives more weight to latest data
        * after inserting new term, we'll go to the terminal node of the phrase and increase its frequency.
          * Since we're storing top 10 queries in each node, it's possible that this termjumped into the top 10 queries in each node
          * we need to update the top 10 queries of those nodes then
          * traverse back from terminal node to the root.
          * For every parent, check if current query is part of top 10
          * If so, update the corresponding frequency
          * else check if current query frequency is high enough to be part of top 10
          * if so insert this term and remove lowest top 10 term
    * How do we remove a term from the trie>
      * due to legal issue, hate, or piracy we need to remove term
        * We can completely remove these nodes during the batch updates
        * we can add a filtering layer as well to remove any such term before sending to users

## Permanent Trie Storage
* How to store trie in a file so that we can rebuild our trie easily?
  * needed when machine restarts
* take periodic snapshots and store to file
* enables us to rebuild a trie if a server goes down
* to store start with the root node and save the trie level by level
  * with each node we can store what character it contains and how many children it has
  * after each node, we should put all of its children
  * ex:
    * “C2,A2,R1,T,P,O1,D”
* we are not storing top suggestions and their counts with each node
* it is hard to store this info, as our trie is being stored top down, we dont have child nodes created before the parent
  * there is no easy way to store their refs
  * for this, we have to recalculate all the top terms with counts
  * can be done while building the trie
  * each node will calculate its top suggestions and pass it to its parent
  * each parent node will merge results from all of its children to figure out its top suggestions

## Scale estimation
* Google sized
* 5 billion searches every day
* 60k queries per second
* there will be a lot of duplicates in 5 billion queries
* Assume 20% are unique
  * if we want to index the top 50% of the search terms, we can get rid of a lot of less frequently searched queries
  * assume we will have 100 million unique terms for which we want to build an index
* storage estimation
  * each query consists of 3 words on average
  * average word is 5 chracters
  * 15 character average query size
  * 2 bytes to store a character
  * 30 bytes for an average query
  * 100 million * 30 bytes = 3 GB
  * expect daily growth in data, removing terms that are not searched anymore
  * assume 2% new queries daily + maintenance for last year
    * 3GB + (0.02 * 3GB * 365 days) => 25GB

## Data partition
* Our index can easily fit on one server
* we can still partition it in order to meet our requirements of higher efficiency and lower latencies
* Range based partitioning
  * store phrases in separate partitions based on their first letter
  * can combine less frequenly used letters into one partition
  * can lead to unbalanced servers
    * ex: too many queries start with E, so E partition is overloaded
* Partition based on maximum capacity of the server
  * partition trie based on maximum memory capacity of servers
  * store data on a server as long as it has mem
  * when subtree cannot fit, break partition there to assign that range to this server and move on to next server
  * first trie stores all terms from A to AABC
  * next server stores from AABD onwards
  * ex:
    * 1 A-AABC
    * 2 AABD - BXA
    * 3 BXB - CDA
  * if the user has typed A
    * queries 1 and 2
  * once they type AAA
    * queries only 1
  * We can have a lb in front of our trie servers to store this mapping and redirect traffic
  * if querying from multiple servers, we need to merge results on server or client
    * if done on server
      * need to introduce another layer of servers between lbs and trie servers
        * called aggregators
        * they will aggregate results from tries servers and return top results
  * partitioning based on capacity can still lead to hot spots
    * lots of queries start with cap
    * they all go to same trie server
* partition based on the hash of the term
  * terms are passed to hash function, hash tells which server
  * randomizes storage, minimizes hotspots
  * disadvantage is we need to ask all servers then aggregate results

## Cache
* caching top query terms will be extremely helpful
* small percentage of queries responsible for most traffic
* cache in front of trie servers with most frequently searched terms and their typeahead suggestions
* app servers hit cache before tries
* ML model can be made to predict engagement on each suggestion
  * based on counting, personalization, trending data
  * cache these terms beforehand

## Replication and LB
* We should have replicas for each trie server for load balancing and fault tolerance
* need a lb to track data partitioning scheme and redirect traffic based on prefix

## Fault Tolerance
* What happens when trie server goes down
  * leader - follower model
    * follower takes over when leader goes down
    * servers that come back can rebuild trie based on snapshot

## Typeahead Client
* client side optimizations
  * client should only hit server if the user has not pressed a key for 50ms
    * debounce
  * if the user is constantly typing, client can cancel inprogress requests
  * client can wait for a few characters before fetching typeahead req
  * clients can pre-fetch some data from the server to save future requests
  * clients can store recent history of suggestions locally
    * recent history has high rate of reuse
  * establishing an early connection with server is important
    * as soon as user opens search engine website, client can open a server connection
      * can save time in establishing connection
  * server can push cache to CSNs and ISPs for efficiency

## Personalization
* receive some typeahead suggestions based on historical searches, location, language, etc
* store personal history of each user separately on server, cache on client
* server can add these personal terms in final set before sending to user
* personal searches should always come first


