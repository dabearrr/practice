# Pastebin

## Attempt at design
### 1 Functional reqs, assumptions, constraints
Functional reqs

* user inputs a large string, gets a shrot link back which they can resolve to get their text back
* can optionally set expiry time
* can optionally set a custom alias
* should it have a max size?

non-functional reqs
* should be highly available
* should be low latency to resolve links

extended funcs:
* analytics on how many times each link has been hit, by who?
* user analytics by country, last_login times
* permissioning system, private / public links

### 2 ballpark estimates
50 m writes / month
100:1 read : write ratio

what can we extrapolate?
500m reads / month

Let's say the average size of a paste is 25kb
that means over 5 years:
5 * 12 * 50m = 3 billion writes over 5 years

30 billion * 25kb = 75 terabytes

QPS?
50m / mo / 30 days / 24 hours / 3600 sec = 20 write requests / second
which means 2000 read requests / second

throughput:
20 * 25kb = 500 kb written / sec
50 mb read / sec

### 3 service apis
write_paste(api_dev_key, paste_text, user_name=None, custom_alias=None, expiry_time=None)
* api_dev_key string
  * used to identify and throttle api clients
* paste_text string
  * data to store under the return short link
* user_name string
  * user who requested the paste, used for analytics
* custom_alias string
  * a optional custom short link, if it is taken already, request will fail
* expiry_time string
  * a optional exiration time for the short link

delete_paste(api_dev_key, short_link)
* used to delete pastes, short_link being the key

### 4 database design
Observations:
* we need to store billions of records
* records have no relations to be managed (other than creator user)
* each object we store is medium sized (pastes can be fairly large)
* service is read heavy
* we will be storing these mappings of URLs to pastes
* if we assume pastes are very large, we may want to consider unstructured storage services instead of direct db storage
  * however, going with db storage for now
* we will store users info as well, in a users table
  * useful for analytics, permissioning

* table 1: URLS table
  * key = short link string
    * used to index into the table and get the paste_text
  * paste_text string
    * stores the main content, the paste text
  * user_name string
    * who posted the short link
  * expiry_time timestamp
    * expiration time of the string
  * create_date timestamp
    * when the entry was created
* table 2 users table
  * key = user_id string
    * unique id for a user
  * user_name string
    * user_name of user
  * email string
    * email of user
  * last_login timestamp
    * last time the user logged in
  * create_date timestamp
    * date the user was created

### 5 basic system design
#### getting the url
##### encoding the paste
* we can encode the paste to get a custom url
* we can use md5 to get a 128 bit value from the paste
* then we can convert this 128 bit value to our url format
* url format can be several bases
  * base 36 a-z0-9
  * base 62 a-zA-Z0-9
  * base 64 a-zA-Z0-9+/
* if we use base64, how long should our links be?
  * using 6 characters, we get 64^6 possible hashes
    * that's 69 billion combinations, which is enough to keep the hash space half open after 5 years
* 6 characters is sufficient
* converting the 128 bit hash to base64, we can then extract our characters from that value
* 2^128 sized number -> base64 6 characters
  * 64^6 <<< 2^128, that means during our base conversion, we will have many extra chars
  * we can just take the first 6 or last 6 characters
* collisions?
  * what if two users have the same paste?
    * at encoding time, we can append a timestamp, user_id, or sequence number to the paste
      * that will ensure different hashes for the paste

##### key pregeneration
* Using a key generation service (kgs) we can have keys all pregenerated for the pastebin
* concurrency issues:
  * a key must be marked as used, so no two pastes can receive the same key
  * as soon as a unused key is fetched, move it from unused to used
* we can have a unused table and a used table
  * unused table has all of the unused keys
    * 69 billion keys * (6 * 1 byte (assuming each alphanum character takes 1 byte)) = 400 GB
  * used table has the used keys
* we can make use of range based partitioning with horizontal scaling
  * nodes will each be given a range of unused keys by some federation system
    * these keys can be pre-marked as used in the main table
    * these nodes can easily give out keys from their ranges
      * without having to check if they are used or requesting a new key from the federation system
    * if they run out of keys to serve, they can request a new range
    * DOWNSIDES:
      * if a host goes down before serving all keys, some keys will be marked as used even though they are not
* key lookup
  * lookup key in used table
    * if found return paste
    * else return 401 error

### 7 data partitioning
* hash based partitioning:
  * can distribute data across nodes using hashes
  * using consistent hashing will insure no hot partitions
* range-based partitioning
  * distribute data based on range
  * can have issues with hot partitioing if certain ranges are more used than others

### 8 caching
* can use solutions like memcached to cache keys for lookup
* nodes can have their own local caches as well
  * if node cache miss, go to memcached
  * if memcached misses, go to db
* what data should we store
  * consider 80 - 20 rule, 20 percent of keys will get 80% of traffic
  * 20% of data will reach 75tb * 0.2 = 15 terabytes of memory needed to cache
  * we will need to use a distributed hash solution, as no regular host has that much mem
  * can adjust based on usage patterns
* cache eviction
  * it would make sense here to use Least recently used as the eviction protocol

### 9 load balancing
* where can we add load balancing?
  * client to backend servers
  * backend servers to cache servers
  * backend servers to database servers
* can use simple round robin to distribute load
  * doesnt consider load
  * can use more complex lb with load in mind

 * purging or db cleanup
  * can delete expired keys or mark as deleted
    * since storage is cheap, we can mark
    * we can delete on lookup, if expiration time is passed on lookup, mark as deleted
    * we can use a lightweight service to delete entries periodically
      * once per day / week, run at low traffic times

# Now the notes from educative
# designing patebin
* store text or images on a url
* share data quickly
## requirements, goals
* functional
    * users can upload or paste their data and get a unique url to access
    * users can only upload text
    * data and links expire by default, users can specify expiration time
    * custom alias
* nonfunctional
  * highly available
  * low latency
  * highly reliable, no data is lost
  * not guessable links
* extended
  * analytics
  * rest apis

## considerations
* similar to tinyurl
* differences
  * limit on text?
    * 10mb limit to prevent abuse
* url size limit?
  * same as tiny url, should impose

## estimates
* read heavy
  * 5 : 1 r:w
* 1m writes / day
  * 12 pastes / sec
* 5m reads / day
  * 60 reads / sec
* storage estimates
  * assume 10kb avg
  * 1m writes * 10kb = 10GB / day
  * over ten years => 36TB
    * 3.6 billion pastes in 10 years
* base64 keys with 6 chars => 64^6 key space = 69 billion
* assuming 1 byte per character, takes 6 * 3.6 billion pastes = 22 GB storage to store 10 years of keys
* 22 GB <<< 36TB
* assuming 70% capacity model
* Bandwidth
  *12 * 10kb = 120kb/s written
  * 600 kb/s read
* memory estimates
  * assuming caching 80 - 20 rule, caching 20% hottest daily reads
    * 20% of 5 million reads / day = 0.2 * 5m * 10kb = 10GB

## system apis
* rest api
```
add_paste(api_dev_key, paste_data, custom_url=None, user_name=None, paste_name=None, expire_date=None)
```
* params
  * api_dev_key string
    * used to throttle requests from bad entities
  * paste_data string
  * custom_url string
  * user_name string
  * paste_name string
  * expire_date string

* returns
  * successful insertion returns url for the paste else error code

```
get_paste(api_dev_key, api_paste_key)
```
returns paste data
```
delete_paste(api_dev_key, api_paste_key)
```
successful delete returns true else false

## database design
* store billions of records
* metadata object is small
* paste object is medium, up to 10mb
* no relations, except for user -> paste map
* read heavy

database schema
* pastes
  * key = url_hash
  * content_key
    * reference to external object holding paste data (s3 arn)
  * expiry_date datetime
  * creation_date datetime
  * user_id: int
* users
  * user_id int
  * name: str
  * email str
  * creation_date datetime
  * last_login datetime

* url_hash is the tinyurl
* content key is a reference to the external object with the paste data

## 7 high level design
* application layer
  * serves read / write requests
* storage layer
  * holds metadata and paste data
  * can segragate these into two storages
    * metadata is structured db
    * storage is unstructured files

## 8 component design
* application layer
  * serves all requests
  * how does it handle a write?
    * option 1 generate key (encoding paste, or random 6 chars)
        * our application server will generate a random six letter string, serving as paste key
          * if no custom alias is passed
        * then we store the contents of the paste in storage, and the metadata in the database
        * after successful insertion, return key
        * problem: duplicate key
          * we can generate a new one, try again until not a dupe
        * if custom alias is a dupe, return error
    * option 2 kgs
      * pregenerate random six letter strings beforehand, stores them in a database
      * when we store a new paste, take a pregenerated key and use it
      * dont need to worry about collision or duplication
      * kgs ensures unique keys
      * can use two tables, one for unused, one for used
      * when app requests a key, move from unused to used
      * kgs can cache some keys in memory
        * these keys are moved to used once loaded to memory
        * if kgs fails, these keys will be mark as used but unallocated
          * can ignore these, should be rare case
      * Problems:
        * KGS is a single point of failure
          * we can keep replicas of KGS in case of failure
        * Can each app server cache some keys from the KGS key database?
          * Yes they can.
          * If application server dies before serving all keys, the un served keys will be lost (marked as used but unallocated)
          * acceptable as we have many keys
        * Handling reads
          * application service layer contacts the datastore
            * if found return paste data
            * else return error
* Data store layer
  * divide into two sections
    * metadata store
      * can use standard SQL db or NoSQL key value document store
    * object storage
      * used to store paste data. can use object storage, like S3 
