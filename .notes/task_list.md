# Task List

This file informs the tasks which need accomplished for this project ranked by high, medium, and low priority.
When a task is completed, move it in to the 'Completed' section.
Tackle tasks from the high priority section first.
Unless explicitly specified, write test cases for each task to verify the requirements are met and automatically run them upon each change.

## Tasks

### High Priority

1. Containerize the URL frontier and the workers.
    * Right now the url frontier and worker components are just python classes. Let's make them run as isolated compute instances we can spin up in docker containers on our machine.
    * Make sure we can launch an arbitrary number of URL frontier and worker containers, and that each container can connect to the external docker resources like redis, mongoDB, etc which we already have.

2. Create controller to connect to and manage external resources and components
    * Add python script
    * Handle command line arguments described in `.notes/project_overview.md`
    * Start up external docker resources if not already online
    * Start up skeleton worker and URl frontier processes successfully
    * 

### Medium Priority

1. Set up resource schema
    * Define MongoDB collections and indexes for link storage
    * Create MinIO bucket structure for content storage
    * Configure Redis data structures for URL queue
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