# Facebook Messenger
## What is fb messenger
* app which provides instant messaging services
* chat with fb friends on phone or web

## requirements and goals
* functional
  * support one-on-one conversations between users
  * track online / offline statuses of users
  * support persistent storage of chat history
* non functional
  * real time chat
  * highly consistent, users see same chat history on all devices
  * high availability; consistency > availablity tho
* extended
  * group chatting
  * push notifications
    * notify users of messages even when offline

## capacity estimation, constraints
* 500m daily active users
* users send 40 messages / ady
* 500m * 40 = 20 billion messages / day

### storage estimation
* average message is 100 bytes
* 20 billion messages * 100 bytes = 2TB / day
* 2 TB * 365 * 5y ~= 3.6 PB
* metadata to store
  * users, messages metadata
* consider replication / data compression as well

### bandwidth estimation
* 2TB data / day
* 25MB / s writes
* read / write ratio should be similar
  * one user writes to another user who reads it
* high level estimates
    * Total messages 	20 billion per day
    * Storage for each day 	2TB
    * Storage for 5 years 	3.6PB
    * Incomming data 	25MB/s
    * Outgoing data 	25MB/s

## High Level Design
* chat server will be main piece
  * orchestrates user communication
  * when a user sends a message to another user, they connect to chat server and send the message to the server
    * server passes message to other user
    * stores it in db as well
* db to hold messages, user and message metadata
### workflow
* user A sends message to User B through chat server
* Server receives the message, sends ack to user A
* server stores the message in db and sends the message to User B
* user b receives the message and sends ack to server
* server notifies user a that message has been delivered to user b

## detailed component design
* simple solution first
* everything runs on one server
* use cases
  * recieve incoming messages and deliver outgoing messages
  * store and retrieve messages from db
  * keep record of which user is online or offline, notify relevant users about the status changes
### message handling
* how to efficiently send / receive messages
  * pull model
    * users periodically ask the server if there are any new messages for them
    * server needs to track messages waiting to be delivered
    * once receiveing user connects to server to ask for new messages, the server returns all pending messages
    * to minimize latency, the user checks the server very frequently
      * most checks will return empty response
      * inefficient, wastes resourcse
  * push model
    * users keep connection open with the server and depend on the server to notify them when new messages come in
    * messages are immediately pushed to users once received by server
    * server does not need to track pending messages
    * minimum latency
  * how do clients maintain an open connection with server?
    * HTTP Long Polling or WebSockets
      * In long polling, clients can request info with expectation that server may not respond immediately
      * if the server has no new data, it hold sthe request open until new data is received
      * then it returns the new data
      * the client then opens a new request, again starting the cycle
      * much better than pull, min latency
      * can timeout after a while, just open a new long poll
  * how can the serrver track all opened connections to redirect messages to the users efficiently?
    * maintain hash table, where key is user_id and value is the connection object
      * when the server receives a message for a user, it looks up the user in the hash table to get the connection
  * what will happen when the server receives a message for an offline user?
    * the server can notify the sender about the delivery failure
    * if it is a temp disconnect (eg receiver's long poll just timed out, about to connect again)
      * ask sender to retry the message
      * retry can be embedded in client logic so they dont have to retype it
      * server can store the message for a while and retry sending it once receiver reconnects
  * how many chat servers do we need?
    * since we have 500m daily, lets plan for 500m connections at any time
    * assuming a modern server can handle 50k connections each, we just need 10k such servers
  * how do we know which server holds the connection to which user?
    * We can introduce a software load blaancer in front of chat servers, that maps each user_id to a server to redirect the request
    * how should the server process a dilver message request
      * store message in db
      * send message to receiver
      * send ack to sender
      * chat server will first find the server that holds the connection for the receiver
      * pass message to that server to send to receiver
      * send ack to sender, store message in db in the background
  * how does the messenger maintain sequencing of the messages
    * we can store a timestamp with each message, which is the time the message is received by the server
    * will not ensure correct orderinbg of messages for clients
    * server timestamp is not always accurate
      * userA sends messageA to server for UserB
      * server receives messagesA at TimeA
      * UserB sends messageB to the server for UserA
      * server receives MessageB at timeB s.t. TimeB > TimeA
      * server sends messageA to userB and messageB to userA
      * so UserA sees MA first then MB, userB sees MB first then MA
    * need to keep a sequence number with every messages for each client
    * seqeunce number determines exact orderingb of messages for each user
    * each client will see different view of the message sequence, but it is consistent across devices
 ### storing and retrieving messages from db
    * whenever chat server gets new message, store in db
      * can either pop a thread to store the message or send an async request to store the message
    * considerations for db
      * efficiently work with db connection pool
      * retry failed requests
      * log failed requests that could not be retried
      * retry the logged failures
    * what storage system should we use?
      * high rate of small updates
      * fetch a range of records quickly
      * lots of small messages to be inserted
      * querys are sequential, access only the newest messages usually
      * Cannot use RBDMS like MySQL or NoSQL like Mongo because we cannot afford to read / write a row from the db every time a user receives / sends a message
      * this would make operations be high latency and create huge db load
      * use Wide Column database solution like HBase
        * column oriented key-value NoSQL db
          * can store multiple values against one key into multiple columns
          * modeled after Google's BigTable
          * runs on top of HDFS
          * HBase groups data together to store new data in a mem buffer, once buffer is full, dump data to disk
          * stores a lot of small data quickly
          * fetching rows by key or scanning ranges of rows is fast as well
          * efficient db to store variable sized data as well, which is required by our server
      * How should clients efficiently fetch data from the server?
        * clients should paginate while fetching data
        * page size can differ by client
          * phones are small screens, thus smaller pages
  ### managing user status
  * need to track online / offline status
  * notify relevant users on status change
  * we can figure out online status from the open connections between server and user
    * the Long polling / websockets
  * 500m active users
    * if we need to broadcast each status change to all relevant active users, it can consume lots of resources
    * optimization
      * on client app start
        * pull status of all friends list users
      * whenever a user sends a message to offline user
        * send failure to sender, update status on client
      * whenever a user comes online, server can broadcast status with few seconds delay
        * incase user just goes offline immediately
      * clients can pull status from the server about users on the current viewport (the screen)
        * should be a infrequent operation
        * we can live with stale statuses for a time
      * whenever the client starts a new chat with another user, we can pull the status at tha time

## Design Summary
* clients open a connection to chat server to send message
* server sends message to receiver
* all active users keep a connection open with server to receive messages
* when new message arrives, chat server pushes it to receiving user with the open connection they have
* messages are stored in HBase
    * supports quick small updates
    * supports range based searches
* servers broadcast online statuses of users to relevant users
* clients can pull statuses of users on client viewport infrequently


## Data partitioning
* lots of data (3.6PB over 5 years)
* Partitioning based on User_id
  * partition based on user_id hash, so a users messages are all on the same db
  * if one shard is 4 TB, we will have 3.6PB / 4TB =~ 900 shards
  * for simplicity lets say we keep 1000 shards
  * get shard by doing user_id % 1000
  * store / retrieve data from there
  * quick to get chat history for any user
* start with fewer db servers with multiple shards on one physical server
* with multiple db instances on a server, we can easilt store multiple partitions on a single server
* hash function needs to understand this logical partitioning
  * so it can map multiple logical partitions on one physical server
* since we will store unlimited history of messages, we start with a big number of logical partitions
  * mapped to fewer physical servers
  * as storage demands increase, we can add more physical servers to distribute logical partitions
* partitioning on message_id
  * if we store different messages of a user on separate db shards, fetching a range of messages of a chat would be very slow, so we should not adopt this scheme

## Cache
* cache a few recent messages in a few recent conversations that are visible in a user's viewport
* since all of a users messages are stored on one shard
  * cache should entriely reside on one machine as well

## load balancing
* need lb at client to chat server level
* maps each user_id to a server that holds the connection of the user and directs the request to that server
* need load balancer for cache servers

## fault tolerance, replication
* what happens when chat server fails
  * they hold connections with users
  * if a server goes down, should we devise a way to transfer the connections
  * it's extremely hard to failover tcp connections ot other servers
  * can jsut have clients to auto reconnect if conenction is lost
* should we store multiple copies of user messages
  * yes
  * we cannot have only one copy of user data
    * if the server goes down permanently or crashes, we cannot recover it
    * store multiple copies of data
    * use reed-solomon encoding to distribute and replicate it

## Extended requirements
* group chats
  * can have separate group chat objects in our system stored on chat servers
  * group chat object has group_chat_id and list of people in chat
  * lb directs group chat messages based on group_chat_id
  * iterate through all users of the chat to find server handling connection of each user to deliver the message
  * store group chats in db partitioned based on group_chat_id
* push notifications
  * current design we can only send messages to active users
  * if user if offline, we send a failure to sender
  * push notifications allow us to send messages to offline users
  * users opt in to get push notifications
  * each manufacturer maintains a set of servers to handle push notifications
  * to handle in our system
    * need a notification server
      * takes messages for offline users
      * sends them to the manufacturer's push notification server, which sends them to users devices







