# Project Overview

## Goal

Build an extensible web crawler. The main goal is building a skeleton which crawls the web, visiting page by page. Users can choose to plug in modules which perform an action when visiting a page. The basic algorithm is:
1. Given a set of URLs, download all the web pages addressed by the URLs.
2. extract URLs from those web pages
3. Add new URLs to the list of URLs to be downloaded. Repeat.

## Architecture

-   **Frontend:** None for now.
-   **Backend:** Uses distributed queues to continue the crawl, worker instances to read from the queues and perform work, caches to hold lightweight information and more durable storage to store already seen content or URLs.

## Key Features

-   Efficient distributed crawl
-   Modular, extensible architecture - users should be able to add new actions to take when a web page is pulled from the queue by a worker
-   Previously seen URLs are ignored, Previously seen content is ignored (within a degree of similarity)
- Workers are stateless
- queues and storage are distributed and fault tolerant
- Web crawl is robust and able to handle bad HTML, unresponsive servers, malicious links, etc.
- Web crawler must be polite (may not make too many requests to a website within a short time interval)

## Constraints

 - Constrain the search to 10000 web pages for now.
 - Do not download or store more than 50mb worth of data for now. If greater than that, abort the search early.
 - Do not download or store images, videos, or PDF, just scrape HTML and text files.
 - Storage should have a 1hr TTL
 - use publicly available APIs and technology instead of creating from scratch where possible

## Interaction and Example flow

1. Start this seed URL and emplace it into the URL Frontier (main queue workers consume from): https://en.wikipedia.org/wiki/Napoleon
2. Workers read from queue and parse the content
    Check if the content has already been seen via content storage
    If so, skip this page
3. Optional step here to 'visit' the page via extensible modules
4. Extract URLs from the rendered webpage
5. Filter malformed URLs or URLs which have already been seen by checking URL storage
6. Emplace all valid, nonvisited URLs into the URL frontier

## In depth design
Below shows a high level design:

![webCrawlerDesign](/architecture/webCrawlerDesign.png)

### Starting the flow:
We want a lightweight python script to initialize the flow.
* **Input**: command line arguments including a seed URL, number of workers, optional extensible module mode (default is NOOP)
* **Output**: Insert message to the URL Frontier.
* **Behavior**:
    1. Initialize all external components - queues, worker instances, databases. Create `num_workers` workers from the command line arguments and assign each worker a unique integer ID in range 0-`num_workers - 1`. Each worker should have the extensible module mode, their worker queue, the URL frontier queue, the content storage, and the link storage resources passed to them via startup arguments or environment variables.
    2. Insert message to URL frontier and start crawl.
    3. Perform logging and monitoring, if necessary.

### Resources needed:

This section describes the external data structures needed for this application commonly used in software development like queues or databases. This section describes the large distributed components needed - unless explicitly mentioned, use cloud provider or docker implementations of these resources, no need to reinvent them. These resources should be fault tolerant and handle concurrent access. They don't need to have a ton of capacity or resources - start with the smallest option available and we can scale them if needed. Each resource will be accessed by multiple components described in later sections.

1. Distributed URL queue
    * **Description**: Distributed queue which holds URLs for processing.
    * **Data structure type**: Queue
    * **Input**: URLs as strings
    * **Constraints**:
        * configurable maximum queue size. Start with max 10000 messages.
2. Content storage
    * **Description** Database which stores HTMl in an efficient manner. Frequent read/write, entries are immutable.
    * **Data structure type** Blob store
    * **Input** HTML. Ideally we store this hashed or in an efficient manner.
    * **Constraints**:
        * We want to be able to efficiently look up if HTML stored in the database is within a degree of similarity to a query HTML.
        * Input HTML will be <= 500kb uncompressed. Ideally less than that with an efficient storage mechanism.
3. Link storage
    * **Description** Database which stores URLs (strings). Frequent read/write, entries are immutable.
    * **Data structure type** set
    * **Input** URLs as strings
    * **Constraints**:
        * Number of input strings can grow large. We want a 1 hr TTL so we don't visit any pages we've already seen.
4. Worker queues
    * **Description**: Distributed queue which holds URLs for processing. Smaller than the Distributed URL queue, specific to one worker (compute instance)
    * **Data structure type**: Queue
    * **Input**: URLs as strings
    * **Constraints**:
        * configurable maximum queue size. Start with max 10000 messages.


### Components needed:

This section describes the components necessary for this application. It contains a description of the component, component inputs, component outputs, dependencies for each component, restrictions, and a list of subcomponents - logical units of functionality each component can be broken down into.

Each component should live in it's own docker or cloud compute instance to distribute compute unless explicitly mentioned. Subcomponents share the same compute instance as the parent component.

1. URL frontier
    * **Description**: Component which reads from Distributed URL queue which holds incoming urls to visit, prioritizes and distributes the URLs to workers.
    * **Input**: URLs as strings.
    * **Output**: URLs to worker queues
    * **Dependencies**: Distributed URL queue, worker instances, worker queues, mapping of queue to worker, mapping of domain to worker.
    * **Behavior**:
        1. Continuously pull URLs from Distributed URL queue.
        2. Prioritize the URL and place in a set of queues ranked by priority.
        3. Consume from this set of queues pseudorandomly, weighted by priority, check if any workers are already handling the domain of the current URL. If they are, publish the URl to that worker's queue. If not, push the URL to the worker under the least amount of load (for now let's assume load is equivalent to number of messages in that worker's queue).
    * **Restrictions**:
        * Handle backpressure from worker queues.
    * **Subcomponents**:
        1. Prioritizer
            * **Description**: consumes from Distributed URL queue, computes priority for each message, pushes to queues q1…qn weighted by priority.
            * **Input**: URLs from URL frontier.
            * **Output**: Populates a set of internal queues which have a global priority. The mapping of priority to queue should be visible to the politeness router.
            * **Dependencies**: Distributed URL queue, PageRank API, weighted queues for message prioritization, mapping table of priority to queue.
            * **Behavior**:
                1. Pull URL from Distributed URL queue
                2. Compute priority for each URL. This should be extensible, we can start with computing the PageRank of a page. This should be accessible via things like an API call. A better pagerank means higher priority. Priorities should be normalized 0 (highest priority) to 100 (lowest priority).
                3. Refer to the table mapping priority to queue to determine which queue to publish this URL to next. Each queue can be responsible for a range of priorities, say `100 % num_queues`
                4. Publish the message to the appropriate queue.
            * **Restrictions**:
                * Be able to handle retries and transient outages from PageRank API
        2. Politeness router
            * **Description**: pulls from queues pseudo-randomly, weighted by priority. consults a table which maps URL domain to worker ID. Then pushes messages to workers
            * **Input**: Reads URLs from prioritized politeness queues
            * **Output**: publish URL to worker queues
            * **Dependencies**: Table which maps workers to domains they are responsible for, politeness queue, table which maps workers to their dedicated queue, worker queues.
            * **Behavior**:
                1. Compute a queue to look up. This should be done by choosing a random number between 0-100, with the caveat that lower numbers are more likely to be chosen. Look up the table mapping priority to queue to determine which queue to read from - since each queue is responsible for a range of priorities, take the floor of the chosen priority to pick the next queue.
                2. Read from the chosen queue and reference the table of domain to worker ID. If it does exist in the table, publish that message to the worker ID the domain maps to. Reference a lookup table of worker id to queue to do so. If it does, push the URL to the worker under the least amount of load (for now let's assume load is equivalent to number of messages in that worker's queue).
            * **Restrictions**:
                * workers only process messages from the same domain, so as to not DDOS any client.
                * in general, higher priority queues are read from first.
                * Worker domain table should have a TTL of 5 minutes.
                * Each worker should have their own dedicated queue they read from.
                * Mapping of worker should be done by worker ID.
2. workers
    * **Description**: Compute instances which download the webpages, parse the content, extract usable links, and potentially perform some action on those links before pushing the new links to the Distributed URL queue.
    * **Input**: URLS from dedicated worker queue
    * **Output**: URLs to Distributed URL queue
    * **Dependencies**: worker queue, Distributed URL queue, content storage, link storage, optional extensible action.
    * **Behavior**:
        1. Pull URL from worker queue
        2. Download webpage.
        3. Validate content, discarding content we've already seen.
        4. Optionally perform some action based on the extensible module plugged in.
        5. extract URLs from the content.
        6. Parse the URLs, discarding already seen or harmful ones.
        7. Publish validated URLs to Distributed URL queue.
    * **Restrictions**:
        * N/A
    * **Subcomponents**:
        1. HTML downloader
            * **Description**: Downloads the html associated with each URL
            * **Input**: URLs from worker queue.
            * **Output**: raw html as text.
            * **Dependencies**: worker queue, URL website
            * **Behavior**:
                1. Pull URL from worker queue
                2. Download HTML associated with the URL
            * **Restrictions**:
                * Handle unresponsive URLs via short timeout with a single retry.
                * Short circuit the HTML download if it is > 500kb.
        2. Content parser
            * **Description**: Parses the HTML from the downloader to determine if we should handle this webpage. Reference content storage for old content and update content storage with new content.
            * **Input**: raw HTMl as text.
            * **Output**: raw HTML as text.
            * **Dependencies**: HTML downloader, content storage
            * **Behavior**:
                1. Validate HTML is well formed.
                2. Check if we have seen the same or similar HTML in the past. This can be done by hashing the HTML and checking the content storage for the same hash, but ideally we check if the HTMl is within a degree of similarity to previously seen HTML. HTML that is 90% similar or more we should ignore and discard this webpage. Otherwise store the HTMl in an efficient format in the content storage and pass along HTML to next component. 
            * **Restrictions**:
                * HTML should be stored efficiently.
                * Be able to handle transient outages in content storage.
        3. Extensible Module
            * **Description**: This is a component that allows the user to plug in different modes to perform some function on the validated HTML. If not specified, this component is a NoOp. This component will perform some side effect on the input HTML like recording a metric, and will output the same validated HTML. The user will specify if alternative functionality is needed via a command line argument - the initial controller python script will be responsible for passing that functionality to the worker instances. Worker instances should initiate the proper extensible module based on the command line argument.
            * **Input**: raw HTML as text.
            * **Output**: raw HTML as text.
            * **Dependencies**: Content parser, Command line arguments.
            * **Behavior**:
                1. Perform side effect on HTMl based on worker instance startup arguments passed by controller command line. If none specified, perform noop.
            * **Restrictions**:
                * N/A
        4. Link extractor
            * **Description**: Pulls links from the HTML, validates them and passes along to the Distributed URL queue, updating link storage.
            * **Input**: raw HTML as text.
            * **Output**: publish message to Distributed URL queue.
            * **Dependencies**: Content parser, Link storage, URL frontier
            * **Behavior**:
                1. Extract links from the raw HTML.
                2. Validate the links are well formed.
                3. Check the Link storage to see if we have already visited this URL or if we have visited it. If we have, drop it, otherwise store this link in the Link storage and publish the URL to the Distributed URL queue.
            * **Restrictions**:
                * Be able to handle malformed links and transient outages in link storage or Distributed URL queue.
