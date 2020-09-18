# Facebook Newsfeed
* newsfeed is the updating list of stories in the middle of fb homepage
* status updates, photos, vids, links, apps, likes from people, pages, groups followed
* compilation of complete scrollabvle version of friends' and your life story
* used in twitter, insta, facebook

## Requirements and Goals
* Newsfeed for Facebook with the follwoing requirements

### Functional requirements
* Newsfeed will be generated based on the posts from the people, pages, and groups that a user follows
* user may have many friends and follow a large number fo pages/groups
* feeds may contain images, videos, or just text
* our service should support appending new posts a they arrive to the newsfeed for all active users

## Non functional requirements
* system should be able to generate any user's newfeed in real time, 2s max
* a post shouldnt take mroe than 5s to make it to a user's feed assuming new newsfeed request comes in

## Capacity Estimation and constraints
* Average user has 300 friends and follows 200 pages

* traffic estimates
  * 300M DAU
  * each fetch timeline 5x a day
  * 1.5B newsfeed requests / day
  * 17500 newsfeed requests /sec
* storage estimates
  * assume 500 posts in every user's feed that we want to keep in mem for quick fetch
  * each post is 1kb in size
  * need 500kb of data per user stored
  * need 150TB mem for all users
  * if a server can hold 100GB we would need aroudn 1500 machines to keep the top 500 posts in mem for all active users


## System APIs
* soap or rest

* get_user_feed(api_dev_key, user_id, since_id, count, max_id, exclude_replies)
  * api_dev_key string
    * throttle requesters
  * user_id number
    * id for user to make newsffeed for
  * since_id number
    * optional, returns results with ID > since_id
  * count
    * optional, number of feed items to fetch, max 200
  * max_id number
    * OP returns results with id < max_id
  * exclude_replies bool
    * optional, prevents replies from appearing in returned timeline
  * returns JSON of feed items


## Database design
* primary objects
  * user
  * entity page / group
  * FeedItem post
* relationships
  * user follows others entities
  * user friends users
  * users and entities can post feeditems with text, imgs, or vids
  * feeditems have a user_id pointing to the user who created it
    * lets assume only users can create feeditems
  * feeditems can have an entity_id pointing to the page or group where that post was created
* User table
  * pk user_id int
  * name varchar
  * email varchar
  * dob datetime
  * creationdate datetime
  * lastlogin datetime
* Entity
  * pk entity_id int
  * name varchar
  * type tinyint
  * description varchar
  * creationdate datetime
  * category smallint
  * phone varchar
  * email varchar
* UserFollow
  * user_id int PK
  * entity_or_friend_id int PK
  * type tinyint
* FeedItem
  * PK feed_item_id
  * user_id int
  * contents varchar
  * entity_id int
  * location_latitude int
  * location_longitude int
  * creation_date datetime
  * num_likes int
* feed_media
  * PK feed_item_id int
  * PK media_id int
* media
  * PK media_id
  * type smallint
  * description varchar
  * path varchar
  * location_lat int
  * location_long int
  * creation_date int
* type identifies if the entity followed is a user or entity

## high level system design
* Feed generation
  *  newfeeds is generated from the posts of followed users / entities
  *  steps to generate feed
     * retrieve ids of all users and entities followed
     * retrieve latest, most popular and relevant posts for those ids
       * these are feed candidates
     * rank these posts based on relevance to jane
       * this represents jane's current feed
     * store this feed in the cache and return top posts to be rendered on jane's feed
     * on the front end, when jane reaches the end of her current feed, she can fetch the next 20 posts from the server, and so on
  * generated feed once, stored in cache
  * what about new incoming posts from people that jane follows
  * if jane is online, we should have a system to rank and add those new posts to her feed
  * we can periodically perform the above steps to rank and add the newer posts to her feed
  * jane can be notified of new feed items to fetch
* Feed publishing
    * jane has to request and pull items for her feed
    * when she reaches the end of her current feed, she can pull again
    * for newer items, the server can notify jane to pull, or push the posts to her
    * high level:
      * web servers: to maintain connection with user
        * used to transfer data to user
      * application server
        * to execute workflows of storing new posts in db servers, also needed to retrieve and push newsfeed to user
      * metadata db and cache
        * to store user, pages, groups metadata
      * posts db and cache
        * to store posts metadata and their content
      * vidoe and photo storage and cache
        * blob storage, to store all the media included in posts
      * newsfeed generation service
        * gather and rank all relevant posts for a user to generate newsfeed and store in cache
        * server will also receive live updates and add these newer feed items to any users timeline
      * feed notification service
        * to notify user that newer items are available
## detailed component design
* feed generation
  * simple case
  * fetch most recent posts from all the users and entities jane follows
  * ```
    (SELECT FeedItemID FROM FeedItem WHERE UserID in (
    SELECT EntityOrFriendID FROM UserFollow WHERE UserID = <current_user_id> and type = 0(user))
    )
    UNION
    (SELECT FeedItemID FROM FeedItem WHERE EntityID in (
        SELECT EntityOrFriendID FROM UserFollow WHERE UserID = <current_user_id> and type = 1(entity))
    )
    ORDER BY CreationDate DESC 
    LIMIT 100
    ```
  * this is very slow
    * especially if many are followed
      * have to sort merge rank
    * we generate it live
    * for live updates, each status update will result in feed updates for all followers
    * this coould result in large backlogs in our newsfeed generation service
    * for live updates, the server pushing newer posts to users could lead to very heavy loads, especially for people or pages with a low of followers
      * can pre generate timeline and store it in mem
* offline newsfeed generation
  * we can have dedicated servers continuously generating users' newfeeds and storing them in memory
  * when a user requests new posts, we just serve the pregenerated feeds
  * compiled on a regular basis, served when requested
  * servers query to see the last time the feed was generated
  * add posts from after that time
  * store this data in a hash table where key is user_id, value is
    * ```
      Struct {
        LinkedHashMap<FeedItemID, FeedItem> feedItems;
        DateTime lastGenerated;
        }
      ```
  * store feed items in linked hashmap or treemap
  * jump to any feed item or iterate easily
  * to fetch more feed items for user, send the last feed item seen in newsfeed
    * we'll take everything after that and return it
  * how many feed items to store in mem
    * initially we can start with 500
    * can be adjusted BASED on USAGE
    * for any user that wishes to see more posts, we can query backend servers
  * should we generate and keep in memory newsfeeds for all users?
    * there will be a lot of users that dont login frequently
    * solutions
      * LRU cache that can remove users from memory that havent accessed their newsfeed in a long time
      * figure out login pattern of user to pregenerate their newsfeeds
        * consider what time and what days of the week the user logs in
* feed publishing
  * pushing post to all followers = fanout
  * push approach is called fanout on write
  * pull approach is fanout on load
  * models
    * Pull model or Fan out on load
      * keep all recent feed data in memory so that users can pull it from the server whenever they need it
      * clients pull feed data regularly or manually
      * problems
        * new data may not be shown until they pull
        * hard to find correct pull cadence
          * most pulls are empty
    * Push model, fan out on write
      * when a user publishes a post, we can immediately push this post to all the followers
      * dont need to go through your friend's list and get feeds for each of them
      * significantly reduces read ops
      * to efficiently handle this, users must maintain a long poll request with server
      * problems can occue with celebrity users
        * they have many followers, huge fan out on write
    * Hybrid
      * stop pushing posts from celebrity users
      * for celebrity users we allow followers to pull the updates
      * we save a lot of resources by disabling push for celebs
      * versatile
    * how many feed items to return per request
      * we should have a max of items a user can fetch (20 for ex)
      * let the client specify, based on viewport
    * should we always notify users of new posts on newsfeed
      * can consider mobile data usage
      * on mobile we can enforce pull
## Feed Ranking
* can use creation_time
* complex
  * select key signals that make a post important
  * likes
  * comments
  * shares
  * time of the update
  * whether the post has images or vids
  * can also consider progress in user stats
    * stickiness, retention, ad revenue

## data partitioning
* sharding posts and metadata
  * tons of new posts per day
  * high read volume
  * need to shard based on tweet_id + creation_time
    * two part id, creation_time then tweet_id
    * has posts sorted by time posted, so we can get most recent fast
* sharding feed data
  * can partition feed data based on user_id
  * can try storing all user data on one server
  * when storing, we pass user_id to hash function to map user to the cache server
  * we expect 500 feed_items max, so we can avoid a user's feed becoming too large and not fitting on a server
  * consistent hashing for growth / replication
