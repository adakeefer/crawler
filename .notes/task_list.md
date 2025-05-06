# Task List

This file informs the tasks which need accomplished for this project ranked by high, medium, and low priority.
When a task is completed, move it in to the 'Completed' section.
Tackle tasks from the high priority section first.
Unless explicitly specified, write test cases for each task to verify the requirements are met and automatically run them upon each change.

## Tasks

### High Priority

1. Patch @init_redis.py to create the queues and caches needed. We specifically want the functionality described in @project_overview.md and @README.md .  The file should take in a command line argument for number of workers (int, default is 2). Create:
    1. The main distributed URL queue using @URLQueueConfig 
    2. queues using @PriorityQueueConfig for each priority_queue described in @URLQueueConfig .
    3. worker queues using @WorkerQueueConfig for each worker. 
2. Create controller to connect to and manage external resources and components
    * Add python class for the controller and a bash script to start the crawl by invoking the controller with the appropriate command line arguments.
    * Handle command line arguments described in `.notes/project_overview.md`
    * Start up all docker resources and run health checks
        * note: We should create as many worker queues as we have `num_workers` passed to the controller at startup via command line argument, using the same data structure for each.
        * controller should establish an immutable mapping of worker id to redis worker queue. each worker gets a unique queue.
        * URL frontier should be passed this mapping as a command line argument upon startup.
        * each worker instance should be passed their unique ID and their unique redis worker queue resource location upon startup
    * Take in the seed URL and feed it to the Distributed URL queue, begin logging and monitoring url frontier and worker container activity.

### Medium Priority

1. Set up resource schema
    * Define MongoDB collections and indexes for link storage
    * Create MinIO bucket structure for content storage
    * Configure Redis data structures for distributed URL queue
    * Configure Redis data structures for worker queues. We should create as many worker queues as we have `num_workers` passed to the controller at startup via command line argument, using the same data structure for each.
2. Implement URL frontier prioritizer subcomponent
3. Implement URL frontier politeness router subcompoment
4. implement worker HTML downloader subcomponent
5. Implement content parser subcomponent
6. Implement Link extractor subcomponent

### Low Priority

1. Add monitoring and metrics on external resources
2. Implement Extensible module subcomponent
3. Add monitoring and metrics on components

### Completed

1. Create external resources
    * Create Distributed URL queue
    * Create Content storage
    * Create link storage
    * Create worker queues

2. Create skeleton worker and URL frontier processes
    * Created worker process that connects to Redis, MongoDB, and MinIO
    * Created URL frontier process that connects to Redis
    * Added comprehensive tests for both components
    * All components print appropriate connection status messages

3. Containerize the URL frontier and the workers.
    * Right now the url frontier and worker components are just python classes. Let's make them run as isolated compute instances we can spin up in docker containers on our machine.
    * Make sure we can launch an arbitrary number of URL frontier and worker containers, and that each container can connect to the external docker resources like redis, mongoDB, etc which we already have.

- Test and debug MongoDB scripts (2024-06-07):
    - Fixed index creation to only pass expireAfterSeconds if present
    - Converted index fields to PyMongo format
    - Patched verification to match MongoDB index naming
    - Used Docker Compose credentials for authentication
    - Confirmed collections and indexes are created and verified