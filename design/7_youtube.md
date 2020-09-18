# Youtube
## Functional Requirements
* users can upload videos
* users can share and view videos
* users can search for videos by title
* we can record stats of videos
* users can add and view comments on videos

## Non functional requirements
* system should be highly reliable, any video uploaded should not be lost
* system should be highly available. consistency can take a hit for availability
  * if a user doesnt see a video for while, its fine
* users should have a real time experience watching videos and should not feel any lag

## out of scope
* video recs
* most popular vids
* channels
* subscriptions
* watch later
* favorites
## capacity estimation
* assume 1.5 billion total users
* 800m DAU
* if on average a user views 5 vids a day
  * 800m * 5 = 4b vids viewed per day / 86400 = 46k views / sec
* assume our read : write ratio is 200:1
  * 46k / 200 = 230 vids uploaded / sec

### Storage estimates
* assuming every minute 500 hours of video is uploaded to youtube
* if one minute of video is 50MB of storage
  * 500 hours * 60 mins * 50MB => 1500 GB / min
    * 25GB / sec
* these numbers are ignoring compression and replication, which would change our numbers

### Bandwidth estimates
* with 500 hours of video uploads per minute and assuming each vid upload takes 10 MB / min bandwidth, we'd get 300GB of uploads every minute
  * 500 hours * 60 mins * 10 MB = 300GB/min (5GB / sec)
* with a read:write ratio of 200:1, we would have 1TB/s outgoing bandwidth

## System APIs
* SOAP or REST Apis to expose our service
* read, write, search
* uploadvideo
  * upload_video(api_dev_key, video_title, video_description, tags, category_id, default_language, recording_details, video_contents)
  * params
    * api_dev_key string
      * dev key for api callers, used to throttle and measure stats
    * video title string
      * title of the vid
    * video_description string optional
    * tags arr optional
      * used for video search
    * category_id str
      * category of the video
    * default_language str
      * default vid language
    * recording_details str
      * location where the vid was recorded
    * video_contents (STREAM)
      * video to be uploaded
* Returns string
  * success message if accepted request
    * once video encoding is complete, user is notified with emailed link to access the video
    * we can also expose a queryable API for users to check upload status
  * http error if failed
* search video
  * search_video(api_dev_key, search_query, user_location, maximum_videos_to_return, page_token)
  * params
    * api_dev_key
    * search_query str
      * string with search query
    * user_location str optinal
    * maximum_videos_to_return int
      * max results to return in one request
    * page_token str
      * token will specify a page in the result set that should be returned
  * returns
    * JSON of matching videos if succeeded
      * video title, thumbnail, video creation date, view count
* stream video
  * stream_video(api_dev_key, video_id, offset, codec, resolution)
  * params
    * api_dev_key
    * video_id str
      * the video to stream
    * offset number
      * time in seconds from the beginning of the video
      * useful to stream from any start point
      * if a user switches devices, they can start at the same point they left off
    * resolution str, codec str
      * used to stream the video in a way that your device supports (pc vs phone have different supported res / codecs)
  * returns a media stream (video chunk) from the given offset


## High Level Design
* Processing queue
  * each uploaded video will be pushed to a processing queue to be dequeued later for encoding, thumbnail generation and storage
* encoder
  * encodes each uploaded video into multiple formats
* thumbnails generator
  * generates a few thumbnails for each video
* video and thumbnail storage
  * store video and thumbnail fiels in distributed file storage
* user database
  * to store user metadata
    * name, email, address
* video metadata storage
  * metadata db to store video metadata
    * title, file_red, uploading userm views, likes, dislikes

## Database schema
* Video metadata storage
  * video id
  * title
  * description
  * size
  * thumbnail
  * uploader
  * likes
  * dislikes
  * views
* Comments
  * video_id
  * comment id
  * user id
  * comment
  * creation_date
* Users
  * uid
  * name
  * dob
  * address
  * email
  * creation date
  * last login

## detailed component design
* read heavy
* where to store vids
  * distributed file system
    * hdfs, glusterFS, S3
* how to efficiently manage read traffic
  * very read heavy
  * split read traffic from write traffic
  * since we will have multiple copies of each video, we can distribute our read traffic on different servers
  * for metadata, we can have master-slave configurations
  * writes go to leader first, then the changes are percolated to other follower servers
  * followers can have stale data, eventually consistent though
* where would thumbnails be stored
  * lot more thumbnails than vids
  * each vid will have 5 thumbnails
  * need a very efficient storage system that can serve huge read traffic
  * two considerations
    * thumbnails are small 5kb files
    * read traffic for thumbnails >> read traffic for vids
      * watch 1 vid at a time
      * searching shows 20 thumbnails at a time
  * can we store them all on a disk?
    * lot of files
    * have to perform many disk seeks to read
    * inefficient
  * Bigtable
    * combines multiple files into one block to store on disk
    * very efficient to read small amount of data
    * both of these pluses are the most significant reqs of our service
    * keep hot thumbnails in cache
    * they are small, so we can cache many of them
* video uploads
  * since vids can be huge, if the connection drops during upload, we should support resuming upload from same point
* video encoding
  * newly uploaded vids are stored on the server
  * new task is added to the processing queue to encode the vid into multiple formats
  * once encoding is done, uploader will be notified and emailed a link to the vid to view / share

## Metadata sharding
* lots of video throughput
* need to distribute our data in a way to optimize read / write operations
* sharding based on user_id
  * we can try sotring all of the data for a user on one server
  * pass uid to hash functionb which maps user to db server which will store that users videos
  * while querying for videos of a users, we can ask our hash function to find the server with that user's data
    * read from there
  * to search vids by title we need to query all servers, each server will return a set of vids
  * a centralized server will aggregate and rank the results
  * issues
    * hot user for reads
      * lot of queries with that users, performance bottleneck
    * hot user for writes
      * guy uploads a ton of vids
      * maintaining a uniform distribution of growing user vids is tricky
* sharding based on video_id
  * hash function maps video_ids to a random server where we store that vids metadata
  * to find videos for a user, we query all servers
  * each server returns a set of vids
  * central server aggreagates and ranks the results
  * solves problem of popular users, shifts it to popular vids
* improve performance with a cache to store hot vids

## video deduplicaiton
* considering a ton of users are uploading lots of vid data, we will have to deal with widespread video deduplication
* duplicate videos often have different aspect ratios or encoding
* might have overlays or borders or be excerpts from original longer video
* proliferation of duplicate videos can impact:
  * data storage
    * wasting storage by storing dupes
  * caching
    * duplicate videos result in degraded cache efficiency by taking up cache space from unique videos
  * network usage
    * duplicate vids increase the amount of data sent over the network to in-network caching systems
  * energy consumption
    * higher storage, inefficient cache, and network usage can result in energy wastage
* user impact
  * duplicate search results, longer vid startup times, interrupt streaming
* service wants to catch duplicates early
* at upload time and not post processing
* inline deduplication will save us a lot of resources in encoding, transfer, and storage
* As soon as a user starts upload a vid, we can run video matching algorithms (block matching, phase correlation) to find duplicates
* if we already have a copy of the vid being uploaded, we can stop the upload and use the existing copy or continue the upload and use the newly uploaded video if it is higher quality
* if the newly uploaded vid is a subpart of an existing vid or vice versa, we can intelligently divide the video into smaller chunks so we only upload the missing parts

## load balancing
* use consistent hashing among cache servers
  * help balance load between cache servers
  * static hash-based scheme to map videos to hostnames
    * can lead to uneven load on logical replicas due to video popularity
    * if a video is popular, that logical replica will experience more traffic than other servers
    * unveven load on logical replicas can translate to uneven load on physical servers
    * to resolve this, we can redirect a client to a less busy server in the same cache location
      * dynamic HTTP redirections
        * drawbacks
          * service tries to load balance locally, which leads to multiple redirections if the host that recieves the redirection cannot server the video
          * each redirection requires a client to make another HTTP request
          * leads to higher delays before playback
          * inter tier (cross data center) redirections lead a client to a distant cache location becuase higher tier caches are only present at a few locations

## cache
* to serve globally distributed users, we need a massive scale video delivery system
* our service should push its content closer to the user using a large number of geographically distributed video cache servers.
* we can cache hot db rows
* memcached
* app servers hit cache before db
* LRU
* more intelligent cache?
  * 80-20 rule
    * store top 20% of daily read volume of videos and metadata

## CDN
* content delivery network
* distributed servers that deliver web content to a user based in the geographic locations of the user, the origin of the web page and a content delivery system
* service can move popular vids to CDNs
  * CDNs replicate content in multiple places
  * better chance of vids being closer to the user, with fewer hops
* CDN machines make heavy use of caching and can mostly serve vids out of memory
* less popular vids can be served by our servers in various data centers

## fault tolerance
* consistent hashing for distribution among database servers
* help in replacing dead servers, distributing load

