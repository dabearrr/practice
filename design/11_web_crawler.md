# Web Crawler
* automated system that browses the web
* collects documents by recursively fetching links from a set of starting pages
* search engines
  * download all webpages to create an index on them
* uses
  * test web pages and links for valid syntax and structure
  * monitor sites to see when their structure or contents change
  * maintain mirror sites for popular web pages
  * search for copyright infringement
  * for special purpose index
    * derive meaning from pages

## requirements and goals
* gotta crawl the whole web
* Scalability
  * service needs to be scalable s.t. it can crawl the entire web and can be used to fetch hundreds of millions of web documents
* Extensibility
  * service should be modular
  * new functionality should be expeccted
    * new document types to download / process in the future

## Design Considerations
* Crawling the web is complex
* Questions
  * Is it a crawler for HTML pages only? Or should we fetch and store other types of media, such as sound files, images, videos, etc?
    * answer can change the design
    * general purpose crawler to download different media types
      * we'd need to break down the parsing module into different sets of modules one for html, one for images, one for vids
        * each module extracts "interesting" info from each media type
      * Assume only HTML for now, should be extensible to other media types
  * What protocols are we looking at? HTTP? FTP links? What different protocols should our crawler handle?
    * assume HTTP
    * it shouldnt be hard to extend the design to use FTP and other protocols later
  * What is the expected number of pages we will crawl? How big will the URL database become?
    * Assume we need to crawl 1 billion websites
    * each website has many URLs
      * Assume 15 billion different web pages
  * What is 'RobotsExclusion' and how should we deal with it?
    * Courteous web crawlers implement robots exclusion protocol
      * webmasters declare parts of their site off-limits to crawlers
      * requires web crawler to fetch robot.txt which contain off-limit pages before downloading any content from the site

## Capacity Esimation, Constraints
* 15 billion pages in 4 weeks
  * 15B / 4 w * 7 days * 86400sec =~ 6200 pages /sec
* storage
  * page sizes are highly variable, but we are dealing with HTML text only
  * assume average page size of 100KB
  * each page we are storing 500 bytes of metadata
  * 15B * (100kb + 500) ~= 1.5 PB
  * Assuming 70% capacity model
    * 1.5PB / 0.7 = 2.14 PB

## High level design
* take a list of seed urls as input
* repeatedly execute the following steps
  * pick url from the unvisited url list
  * determine the ip address of its hostname
  * establish connection to the host to download the document
  * parse the document contents to look for new urls.
  * add the new urls to the list of unvisited urls
  * process the downloaded document
    * store it or index its contents
  * go back to tep 1

### How to crawl
* breadth first or depth first?
  * usually BFS is used
  * dfs can be used in some situations
    * if you already established a connection with the website, your crawler may just dfs all the urls in this website to save handshaking overhead
* path ascending crawling
  * can help discover a lot fo isolated resources or resourcse for which no inbound link would have been found in regular crawling of a particular website
  * crawler ascends to every path in each url it intends to crawl
    * example:
      * given seed of http://foo.com/a/b/page.html
        * it crawls /a/b/, /a/ and /

### Difficulties in implementing efficient web crawler
* There are two important characteristics of the Web that makes web crawling hard
  * Large volume of web pages
    * a large volume of web pages implies that web crawler can only download a fraction off the web pages at any time and hence it is critical that the web crawler be intelligent enough to prioritize download
  * Rate of change on web pages
    * web pages change very frequently
    * by the time the crawler is downloading the last page from a site, the page may change, or a new page may be added

* At bare minimum a web crawler needs
  * URL Frontier
    * Store the list of URLs to download and also prioritize which URLs to crawl first
  * HTML Fetcher
    * retrieves web pages from the server
  * Extractor
    * extract links from HTML documents
  * Duplicate Eliminator
    * to make sure the same content is not extracted twice unintentionally
  * Datastore
    * to store retrieved pages, URLs, and other metadata

### Detailed Component Design
* Assume our crawler is running on one server
* crawling is done by working threads
* each thread performs all the steps needed to download and process a document in a loop
* first step
  * remove an absolute url from the shared url frontier
  * absolute url begins with a scheme (Ex: HTTP) which identifies the network protocol to use to download it
  * implement these protocols in a modular way for extensibility
    * if we need to support more protocols later, should be easy
  * based on url scheme, the worker calls the appropriate protocol module to download the doc
  * after downloading, the doc is placed into a document input stream DIS
  * putting documents into DIS will enable other modules to re-read the doc multiple times
* Once the doc is written to the DIS, the worker thread invokes the dedupe test to determine whether this document has been seen before
  * if so, the document is not processed any further and the worker removes the next url from the frontier
* Next our crawler needs to process the downloaded doc
* each doc can have a different MIME type
  * html page, image, video, etc
  * we can implement these MIME schemes in a modular way
    * if we need to support more MIME types, it should be easy to implement
  * based on the download doc's MIME type, the worker invokes the process method of each processing module associated with that MIME type
* Our HTML processing module will also extract all links from the page
  * each link is converted into an absolute URL and tested against a user-supplied URL filter (robot.txt) to determine if it should be downloaded
  * If the URL passes the filter, the worker performs the URL-seen test, which checks if the URL has been seen before
    * means that it is in the frontier or has been downloaded already
    * if it is new, it is added to frontier

### URL Frontier
* data structure that contains all URLs that remain to be downloaded
  * crawl by performing a BFS traversal of the web
    * start from the SEED set pages
    * traversal is easilt implemented with FIFO queue
* since we have a huge list of URLs we can distribute our URL frontier into multiple servers
* each server has many worker threads crawling
* hash function maps each URL to a server responsible for crawling it
* Politeness requirements
  * crawler should not overload a server by downloading a lot of pages from it
  * we should not have multiple machines connecting to a web server
* crawler can have a collection of distinct FIFO subqueues on each server
* each worker thread has its own sub queue
  * workers pull from their own queue
  * when a new url needs to be added, the fifo sub queue that receives it is determined by a hash of the URL's canonical hostname
  * hash maps hostnames to a worker thread number
  * Worker subqueues + hash mapping hostnames to workers leads to having at most one worker thread per given web server
    * this means we avoid overloading a web server
* How big will our URL Frontier be?
  * hundreds of millions of URLs
  * need to store our URLs on a disk
  * implement our queues in such a way that they have separate buffers for enqueuing and dequeueing
  * enqueue buffer dumps to disk once filled
  * dequeue buffer keeps a cache of URLs that need to be visited
  * can periodically read from disk to fill the buffer
* The fetcher module
  * downloads the document corresponding to a given URL
    * uses appropriate network protocol
    * webmasters create robot.txt
      * to avoid downloading the file on every request, our crawler's HTTP protocol module can maintain a fixed size cache mapping hostnames to their robot's exclusion rules
* Document input stream
  * design enables the same doc to be processed by multiple processing modules
  * to avoid downloading a doc multiple times, we cache the doc locally using an abstraction called a Document input stream
  * DIS is an input steam
    * caches the entire contents of the doc read from the itnernet
    * provides methods to reread the doc
    * DIS can cahce small docs entirely in mem
    * larger docs can be temporarily written to a backing file
  * each worker thread has its own DIS
    * reuses from doc to doc
    * after extracting a URL from the frontier
      * worker passes that URL to the relevant protocol module
        * initializes the DIS from a network connection to contain the doc's contents
        * worker then passes the DIS to all relevant processing modules
* Document Dedupe test
  * many docs on the web are available under multiple different URLs
  * docs can be mirrored on different servers
  * these make a crawler download the same doc multiple times
  * to prevent processing a doc more than once, we perform a dedupe test on each doc
  * calculate a 64bit checksum of each processed document and store it in a database
  * for every new document, compare its checksum to allpreviously calculated checksums to see if the doc has been seen
    * md5 or sha
  * how big is checksum db
    * 15b * 8 bytes => 120GB
  * can fit into a modern day server's mem
    * if we dont have enough mem, we can keep smaller LRU cache on each server with everything backed by persistent storage
    * dedupe test checks if checksum is in cache
    * if not is checks in db
    * if checksum found, we ignore the doc
    * else add to the cache and db
* URL Filters
  *  customizable way to control set of USLs to download
  *  blacklist websites to ignore
  *  before addinging each URL to frontier, worker consults the user-supllied URL filter
  *  can define filters to restrict URLs by domain, prefix or protocol type
*  Domain name res
   *  Before contacing a web server web crawler must use the DNS to map the hostname into an ip address
   *  dns name resolution will be a big bottleneck of our crawlers given the amount of URLs we will be working with
   *  to avoid repeated requests, we can start caching DNS results by building a local DNS server
*  URL dedupe tests
   *  while extracting links, web crawlers will encounter multiple links to the same doc
   *  to avoid downloading and processing a doc multiple times, we have to do a url dedupe test
      * store all urls seen by our crawlers in canonical form in a db
      * to save space we store a checksum in place of full text url
      * to reduce operation on the db, we keep a in memory cache of popular urls on each host shared by all threads
      * cache is good for hot URLs
        * will get many hits
      * storage for URLs store
        * checksum is for URL dedupe
        * need a unique set of checksums of all previously seen URLs
        * 15b URLs, 4 byte checksum
          * 15B * 4 bytes => 60 GB
      * bloom filter for deduping
        * bloom filters are a probabilistic data structure for set membership testing
        * may yield false positives
        * large bit vector represents the set
        * element is added to the set by computing n hash functions of the element and setting the corresponding bits
        * element is in the set if the bits at all n locations are set
        * hence false positives
        * false negatives are not possible
        * ISSUES
          * false positives will cause the URL to not be added to the frontier
          * doc is never downloaded
          * false postive chance can be reduced with larger bloom filters
* Checkpointing
  * crawl takes weeks to complete
  * to guard against failures the crawler can write snapshots of its state to disk
  * interrupted or aborted crawl can be resumed easily


## Fault tolerance
* consistent hashing for distribution among crawling servers
* helps for replacing dead hosts
* all crawling servers will be performing regular checkpointing and storing their fofo queues to disks
* if a server goes down, we can replace it
* consistent hashing should shift load to other srevers

## data partitioning
* 3 kinds of data
  * urls to visit
  * url checksums for dedupe
  * doc checksums for dedupe
* we are distributing urls based on hostnames
* we can store the 3 kinds of data on same host
  * each host stores
    * its set of urls to visit
    * checksums of all previously visited URLs
    * checksums of downloaded docs
* consistent hashing
  * urls will be redistributed from overloaded hosts
* each host performs checkpointing periodically
* dump snapshot onto remote server
* if a server dies, another can replace it using snapshot
## crawler traps
* URL that cause a crawler to crawl indefinitely
* some traps are unintentional
* sym link in a fs can create a cycle
* others can be intentional
  * people write traps that dynamically generate infinite web of docs
  * anti spam traps catch spammer crawlers
  * other sites use traps to trick search engines to boost their search rating
