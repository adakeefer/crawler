# Directory Structure

This file describes the logical structure of the project. Please add to it when necessary and consult me on any changes. It is just a starting point for now, the rest of the structure should be inferred from `.notes/project_overview.md`.

## Important Notes
- All directories listed in this file should be created if they don't exist
- Components should be organized in their own directories under `crawler/components/`
- Each component directory should contain its main implementation file and any component-specific tests

## Logical Structure (make any changes below here)

* crawler
    * components
        * worker
            * worker.py
            * Dockerfile
            * requirements.txt
        * url_frontier
            * url_frontier.py
            * Dockerfile
            * requirements.txt
    * tests
        * test_components.py
        * test_infrastructure.py
    * scripts
        * start_crawler.sh
        * run_tests.sh
* docker
    * docker-compose.yml
    * README.md