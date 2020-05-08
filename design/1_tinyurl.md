# Tinyurl design

## 2 Functional requirements

Given a URL, our service generates a shorter unique alias of it

when users access a short link, they should be reirected to the original link
users should optionally be able to pick a custom short link for their url

links will expire after a standard default timespan. Users should be able to specify a exiration timespan


non functional requirementsthe system should be highly avilable
url redirection should happen in real time, low latency
short links should not be guessable

extended reqs:
analytics
rest api calls

## 3 capacity estimation
System is read heavy
100:1 read : write ratio

500M URL shortenings per month
means 50B reads

QPS?
500m / 30 days / 24 hours/ 3600 seconds = ~200 urls written / s
-> ~20000 redirections / s

over 5 years, we expect to store 500m * 5y * 12m = 30 billion URLS
assume each stored object is around 500 bytes
that is 15tb storage

Bandwidth estimates:
200 new URLs / s, * 500 bytes = 100kb/s of data written

20000 redirections / s * 500 bytes = 10 mb/s of data read

Memory estimates:
if we want to cache some of the hot URLs that are frequently accessed, how much memory will we need to store them?
80-20 rule:
20% of the URLs generate 80% of the traffic

we can cache these 20% of urls
20000 reads / sec * 3600 seconds * 24 hours = ~1.7 billion read requests / day

to cache 20% of these requests, we will need 170GB of memory
0.2 * 1.7 billion * 500 bytes

High level estimates:
assuming 500m new URLs per month, with 100:1 read:write ratio

## 4 System APIs:
once we've finalized requirements, it's always a good idea to define the system APIs. This should explicitly state what is expected from the system.

my idea:
get_short_url(original_url, expiry, custom_url)
evaluate_short_url(short_url)

book:
create_url(api_dev_key, original_url, custom_alias=None, user_name=None, expire_date=None)

parameters:
* api_dev_key  (string): the API developer key of a register account. This will be used to, among other things, throttle users based on allocated quota
* original_url (string): the original url to be shorted
* custom_alias (string): a custom alias to be used for the URL
* user_name (string): Optional user name to be used in the encoding
* expire_date (string): Optional expiration date for the short url

Returns: (string)
A successful insertion returns the shorted url, else it returns an error code

delete_url(api_dev_key, url_key)
* Where "url_key" is a string representing the short url
* A successful deletion returns 'URL Removed'

How do we detect and prevent abuse:
* A malicious user can put us out of business by consuming all URL keys in the current design. To prevent abuse, we can limit users via their api_dev_key.
  * Each api_dev_key can be limited to a certain number of URL creations and redirections per some time period.

## 5 Database Design
* Defining the DB schema in the early stages of the itnerview would help to understand the data flow among various compenents and later would guide towards data partitioning.

Observations:
* we need to store billions of records
* each object we store is small (less than 1k)
* there are no relationships between records, other than storing the creator of a URL
* our service is read heavy

Schema:
* We will need a URL table
  * Primary key is the hashed url
  * the original url is an attr
  * creation_date
  * expiration_date
  * user_id
* We'll need a users table to store who created the short links
  * pk = user_id
  * name
  * email
  * creation_date
  * last_login

What kind of database should we use?
considering the volume of requests and the lack of relationships

NoSQL is best here

## 6 Basic System Design
### encoding actual url
* We can compute a unique hash of the give nURL (MD5 or SHA256)
* The hash can then be encoded for displaying
* For encodings, we can use base36 or base62 (a-z0-9 vs a-zA-Z0-9) or even base64 (a-zA-Z0-9 and +/)
* A reasonable question to ask: what should the length of the short link be
  * using base 64, 6 characters is 6^64 = 69 billion strings
  * 8^64 is ~281 trillion possible strings

Lets assume 6 characters is enough with 69b strings

* using MD5, we get a 128 bit hash value.
* after base64 encoding, we get a string with more than 21 characters (each base64 character encodes 6 bits of the hash value)
* since we are using 6 letters for short links, which characters of the 21 should we use?
  * we can use the first 6 letters.
  * this could result in key duplication, to resolve that, we can shoose some other characters out of the encoding string or swap some characters

Issue with the solution?
* if multiple users input the same original url, get same short link
* what if parts of the url are encoded?

Workarounds:
* append seq number to URL before generation
* append user id
  * requires sign in or user input uniqueness key
    * may still get conflict

###  Generating keys offline
* can use a key generation service (kgs), which generates random six letter strings beforehand and stores them
* whenever a new url is requested, we can use one of these pregenerated urls and mark as used
* Concurrency issues
  * as soon as a key is used, it should be marked as used
  * it can be split into two tables, not-used and used
  * as soon as a key is requested, it is moved to used and then returned
* kgs service can keep some unused keys in memory, ready to be used
* performance improvement: as soon as keys are loaded to memory, they are put in used table
* kgs has to make sure to not give the same keys to multiple servers
  * it must obtain a lock on the data structure holding the unused keys before pulling them
* key db size:
  * base64 encoding, we can precompute all 69b keys
    * assuming each alphanumeric character is one byte:
    * it will take 69b * 6bytes = 400 GB
* KGS is a single point of failure
  * we can keep standby replicas of KGS in case of failure
  * if the primary server fails we fall back to server 2
* caching some keys on server apps:
  * yes, we can cache some section of keys on servers; however, if the server dies before serving all keys given, we may lose those unused keys
* key lookup
  * we can look up the key in our db to get the full url
    * if found, redirect to full url http 302
    * else 404
  * custom alias size limits?
    * can limit to 16 chars

## 7 Data partitioning
* Range-based partitioning
  * partitions containing all data starting with 'a', then 'b' ...
  * can have imbalanced partitions if many urls start with the same char
* Hash-based partitioning
  * take a hash of the object that is being stored
  * choose partition based on ash
  * randomly distributes urls into partitions
  * can still lead to overloaded partitions, which can be solved using "Consistent Hashing"

## 8 Cache
* can frequently used urls
  * memcached, can store full urls with their respective hashes
  * servers hit cache before hitting backend storage
* memory required?
  * we can start by caching the top 20% most used urls
  * based on usage patterns we can adjust
  * 170GB to store 20% of daily traffic
  * can be done on one large machine, or many small ones
* Cache eviction policies to consider
  * want hotter urls to stay in cache
  * Least recently used
    * linkedhashmap type structure
  * replicate caching servers to distribute load
* how to update cache replicas
  * on cache miss, servers hit the backend database
    * we can update the cache when this happens, and pass the new entry to the replicas as well
      * each replica can update its cache by adding the enew entry

## 9 Laod Balancer
* we can add a load balancing layer at three places
  * between clients and application servers
  * between application servers and database servers
  * between application servers and cache servers
* can use simple round robin to distribute reqs
  * does not take server load into account
  * if a server is overloaded or low, lb will keep hitting it
  * can consider more complex LB solution in this case

## Purging or DB cleanup
* Should entries stick around fover, or be purged?
* what happens when expiry is reached
* actively searching for exipred links is a lot of database pressure
* can do lazy cleanup
  * when user accesses expired link, delete it
  * a cleanup service can run periodically to remove expired links
    * should be lightweight and run at low traffic times
* can have a default expiry time
* after removing an expired link, we can put the key back into the unused table to be reused
* should we remove links not accessed in 6 months?
  * storage is cheap, so we can keep

## 11 Telemetry
* track amount of reads
* user locations
* should we store in one row for a url? what happens with popular links being hit many, many times concurrently?
* useful stats:
  * country
  * date/ time of access
  * web page that refers the click
  * browser / platform used to access

## 12 security / permissions
* can users make private urls
* can store permission type of link, private / public
* can create a separate table of url -> authorized readers
* if unauthorized user accesses url, send a 401 error
* key is hash, columns have authorized users

