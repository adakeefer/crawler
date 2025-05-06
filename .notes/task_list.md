# Task List

This file informs the tasks which need accomplished for this project ranked by high, medium, and low priority.
When a task is completed, move it in to the 'Completed' section.
Tackle tasks from the high priority section first.
Unless explicitly specified, write test cases for each task to verify the requirements are met and automatically run them upon each change.

## Tasks

### High Priority

1. Create external resources
    * Create Distributed URL queue
    * Create Content storage
    * Create link storage
    * Create worker queues
2. Create skeleton worker and URL frontier processes
    * The components can just start up in docker containers or cloud compute instances and print a hello message, no need to perform any deeper functionality yet.
    * Components should be able to connect to the appropriate external resources we just created, like content storage or queues. Print a success message when all connections have been made.
3. Create controller to connect to and manage external resources and components
    * Add python script
    * Handle command line arguments.
    * Connect to external resources successfully
    * Start up skeleton worker and URl frontier processes successfully

### Medium Priority

1. Implement URL frontier prioritizer subcomponent
2. Implement URL frontier politeness router subcompoment
3. implement worker HTML downloader subcomponent
4. Implement content parser subcomponent
5. Implement Link extractor subcomponent

### Low Priority

1. Add monitoring and metrics on external resources
2. Implement Extensible module subcomponent
3. Add monitoring and metrics on components