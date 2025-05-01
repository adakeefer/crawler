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

![webCrawlerDesign](architecture/webCrawlerDesign.png)

### Components needed:

1. URL frontier: basically main (big) queue that has stuff partially on disk. This should be a DB
    1. URL frontier is one node that talks to disk and queue, then sends off to other distributed queues
2. Prioritizer
    1. consumes from queue
    2. computes priority for each message, pushes to queues q1…qn weighted by p
3. Politeness router
    1. pulls from queues randomly based on priority. consults mapping table for domains.
    2. pushes messages to workers - workers only process messages from the same domain, so as to not DDOS any client.

From here down, workers handle the rest!

1. HTML downloader
	1. Pulls the actual web page. Maybe renders embedded JS.
    2. Optional: DNS cache
2. content parser
    1. Validate content
    2. Check if we've seen this content before via Blob Storage
    3. Module plugin
    	1. This is where the actual "job" of the web crawler is done. Sometimes you archive pages, sometimes you rank them... the point is the crawler is extensible.
3. Link extractor
	1. Detect and pull links from the HTML
4. link filter
    1. Validate this is a well-formed link
    2. Check if we've seen this link before via URL storage.
    3. If both checks pass, publish the URL to the frontier!

### URL Frontier design
Below shows the design of the url frontier - how we begin, prioritize, and distribute our workload to workers.

![urlFrontierDesign_expanded](architecture/urlFrontierDesign_expanded.png)

* Prioritizers consume from URL queue and decide which pages are worth visiting based on PageRank
* Pages with higher PageRank are published to higher priority queues, with a degree of randomness to avoid hotspots.
* Politeness router pulls from queues based on weights - higher priority queues are more likely to be chosen
* upon choosing a queue and receiving a message, the URL is stripped for the domain and if any worker is already handling pages for that domain the url always goes to that worker to reduce the volume of requests per minute to any specific host. 
    * Maintain a lightweight cache between workers to check this mapping
* Each worker has its own dedicated queue
