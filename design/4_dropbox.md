# Designing Dropbox

## 1 Why Cloud Storage?
* Data is available anywhere anytime
* cloud storage is 100% reliable and durable
* Cloud storage has unlimited space, scales really well

## 2 Requirements, Goals
* Users should be able to upload and download their files from any device
* Users should be able to share files or folders with other users
* Our service should support automatic sync between devices
* The system should support storing large files up to 1 GB
* ACID-ity is required. Atomicity, Consistency, Isolation, Durability of all file ops should be guaranteed
* System should support offline editing. Sync occurs once online

Extended Reqs
* System should support snapshotting of the data

## 3 Some Design Considerations
* expect huge read and write volumes
* Read to write ratio is equal
* files can be stored in small parts or chunks. This can provide lots of benefits
  * failed operations are only retried for smaller parts  of a file. If a user fails to upload a file, only failing chunks are retried
  * reduce data exchange by only transferring data chunks
  * remove duplicate chunks to save storage and bandwidth
  * keep a local copy of metadata with the client to save round trips to server
  * for small changes, clients can upload the diffs instead of the whole chunk

## 4 Capacity Estimationm Constraints
* 500M total users
* 100M daily active users
* user connects from 3 devices on average
* user has 200 files on average, 100 billion total files
* average file size is 100KB, which result in 10PB total storage
* one million active connections per minute

## 5 High Level Design
* User specifies a folder as the workspace
  * any file or folder in this workspace is synced to the cloud
* need to store files and their metadata
  * metadata includes
    * file name, folder name, file size, shared people
* Have three servers
  * Block Server
    * Handles interactions with file storage
  * Metadata Server
    * Handles metadata updates, works with Synchronization service
  * Synchronization service
    *  Handles sync to and from all devices
    *  notifies all clients about changes to their workspace files / folders

## 6 Component Design
### Client
* client application monitors the workspace folder on the user's machine and syncs all files / folders in it with remote cloud storage
* works with storage servers to download, upload, modify files
* works with sync service to handle metadata updates
  * file name, size, modification date
* essential operations:
  * upload and download files
  * detect file changes in the workspace folder
  * handle conflicts due to offline or concurrent updates
  * Handling File Transfer
    * we can break files into chunks
    * use fixed size 4MB for example
      * or calculate optimal chunk size
        * based on storage devices we use in the cloud, optimize space utilization, I/O ops
        * Network bandwidth
        * average file size in storage
    * In metadata, we must track each file and their chunks
* should we keep a copy of metadata with client?
  * yes
    * it enables offline updates and saves time from round trips to update remote metadata
* how do clients efficiently listen to changes happening with other clients?
  * can poll for updates from the server
    * there will be a delay in reflecting changes due to gap in polling
    * waste of bandwidth to poll when there is no update, not scalable
  * can use HTTP long polling
    * client requests info
    * server keeps http request open until new data is available
    * client can again request info immediately after
  * client has 4 parts
    * Internal Metadata database tracks files, chunks, versions, location in file system
    * chunker splits the files into smaller pieces.
      * constructs files from chunks
      * detects parts of the files that have been modified, only transfer those chunks to the cloud
        * saves bandwidth and sync time
    * watcher will monitor local workspace folders and notify the Indexer of any action performed by users
      * when a user creates, deletes, updates files or folders
      * watcher also listens to any changes happening on other devices broadcasted by sync service
    * indexer processes events received from the watcher
      * updates the internal metadata db with the modified chunk information.
      * Once chunks are successfully submitted / download ed to cloud storage, indexer tells sync service to broadcase changes to other clients
        * also updates remote metadata db
    * How do clients handle slow servers?
      *  Exponential backoff
    *  mobile clients sync immediately?
       * they should only sync on demand to avoid mobile bandwidth usage.

  ### Metadata Database
  * versioning, metadata info about files / chunks, users, and workspaces
  * can be relational or NoSQL
  * Should provide consistent view of the files using a db
    * especially if more than one user is working on a file
  * NoSQL dbs are not ACID
    * we would need to support ACID programmatically in our db interactions in the sync service
  * relational db simplifies this logic
  * metadata db:
    * chunks
    * files
    * users
    * devices
    * workspace

  ### Sync service
  * process file updates from clients
  * applies the changes to other clients
  * syncs clients local databases with remote metadata db
  * most important part of the system
    * manages metadata
    * syncs
  * desktop clients use sync service to get updates from cloud
    * or send fies and updates to cloud storage / other users
  * If a client was offline for a period, it polls the system for new updates once online
  * when the sync service gets an update request
    * checks with metadata db for consistency, then performs update
    * then sends a notification to all subscribed devices or users
  * sync service should transmit minimal data between clients and cloud storage for better response time
  * sync service can use a diff algorithm to reduce amount of data to sync
  * Instead of transmitting entire files, we transmit the diff between two file versions
  * only the part of the file that has been changed is transmitted
  * reduces bandwidth consumption and cloud data storage for the end user
  * this is done by chunking the file into fixed size chunks of 4MB
    * then we only transfer changed chunks
  * server and clients can hash the files to see if they need to update the local copy of a chunk or not
  * on the server, if we already have a chunk with a similar hash (even from a different user), we can reuse that same chunk instead of creating a new copy
  * consider using middleware between clients and the sync service
    * should provide scalable message queuing and change notifications to support a high number of clients with pull or push strategies
    * then multiple sync service instances can receive requests from a global request queue, and the middle balances load

### message queuing ervice
* should handle MANY MANY requests
* should support async message based communication between clients and the sync service
* support loosly coupled message based communication between distributed system components
* efficiently store any amount of messages in highly available, scalable queue
* Two queue types, one for requests, one for responses
    * request queue is a global queue, all clients share it
        * client update requests are sent to the request queue
        * sync service pulls request messages to update metadata
    * response queue
      * correspond to individual subscribed clients
    * deliver update messages to clients
    * messages are deleted once received, so we need queues for each subscribed client

### cloud / block storage
* stores chunks of files
* clients interact with storage to send and received objects
* separation of metadata and storage allows use to use any storage db either from cloud or inhouse


## File processing workflow
* Client A updates a file shared with client b and c
* if other clients are not online at update time, message queueing service keeps update notifications in separate response queues for them until they come online
  * A uploads chunks to cloud storage
  * A updates metadata and commits changes
  * A gets confirmation and notifications are sent to B and C about the changes
  * B and C receive metadata changes and download updated chunks


## Data deduplication
* used to eliminate duplicate copies of data to improve storage utilization
* can be applied to network data transfers as well to reduce bytes to upload
* for each new incoming chunk
  * calculate hash
  * compare hash to all hashes of existing chunks to see if we already have that chunk in storage
* two types of dedupe methods
  * Post-process dedupe
    * We can always upload new chunks to storage
    * some separate process will analyze updated data, looking for duplication
    * clients will not have to wait for hash calculation and lookup
    * we will store duplicate data temporarily
    * duplicate data will consume extra bandwidth on transfer
  * Inline dedupe
    *  calculate hash in real time when clients enter data on device
    *  if chunk is already stored, only a ref is added to the metadata, rather than uploading the chunk and adding that ref
    *  optimal network and storage usage

## Metadata partitioning
* need partitioning to scale metadata db
* vertical partitioning
  * store tables related to one feature on one server
    * all user tables on one database
    * all files and chuinks tables on another database
    * will we have scale issues?
      * what if chunks table is too big to store all the records
    * joining two tables in different databases can cause performance / consistency issues
      * how frequently do we join user and file tables?
* range based partitioning
  * store files / chunks based on first character of file path
  * can combine less frequently used letters into one partition
  * can lead to unbalanced servers
    * all files start with E
* hash based partitioning
  * take hash of object to store
  * use hash to figure out db partition
  * hash file_id to get the partition
  * randomly distributes objects
  * need  to use consistent hashing

## 10 Caching
* can have two types of caches
  * file / chunk cache
    * stores hot files / chunks
    * memcached
    * chunks by id / hash
    * block servers hit cache before db
    * big server can have 144GB mem, one such server stores 36K chunks
    * LRU policy
  * metadata cache

## 11 Load balancer
* two locations
  * client -> block server LB
  * client -> metadata server LB
  * use round robin to distribute requests
    * simple, no overhead
    * ignores dead servers
  * can use complex LB which accounts for server load

$$ 12 Security, permissioning, sharing
* store permissions in metadata db
