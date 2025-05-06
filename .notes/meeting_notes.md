# Meeting Notes

## 2024-03-26: Infrastructure Setup

### Completed Tasks
- Set up core infrastructure using Docker Compose:
  - Redis for URL queue and worker coordination
  - MinIO for content storage (S3-compatible)
  - MongoDB for link storage
- Created test script to verify infrastructure connections
- Set up Python virtual environment using UV
- Added requirements.txt with necessary dependencies

### Technical Decisions
- Chose Redis for URL queue due to its simplicity and performance
- Selected MinIO for S3-compatible storage to allow local development
- Used MongoDB for link storage to handle graph-like data structures
- Implemented health checks for all services
- Used UV for Python package management as per tech stack requirements

### Next Steps
- Consider adding specific configurations for each service
- Set up initial data structures in MongoDB
- Create default buckets in MinIO
- Begin implementing URL frontier and worker components

### Notes
- Always consult code-style.mdc, core-development-guidelines.mdc, and tech-stack.mdc for basic rules
- Infrastructure is ready for development with all services running and tested

## 2024-03-26: Test Infrastructure

### Completed Tasks
- Created test runner script using pytest
- Fixed infrastructure tests to use proper assertions
- Added Python-specific patterns to .gitignore
- Set up proper test environment with pytest configuration

### Technical Decisions
- Used pytest with flags:
  - `-x`: stop on first failure
  - `-v`: verbose output
  - `--lf`: run last failed tests first
- Improved test assertions for better error reporting
- Fixed MinIO test to handle empty bucket list case

### Notes
- All infrastructure tests passing
- Test runner script available at `crawler/scripts/run_tests.py`
- Virtual environment properly configured with UV and pytest
