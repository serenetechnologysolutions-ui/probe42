# Implementation Plan: Probe42 Company Data Console

## Overview

Implement a Python console application that fetches company data from the Probe42 API and stores it in MySQL. The implementation uses `requests` for HTTP, `mysql-connector-python` for database operations, and `hypothesis` for property-based testing.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create project directory with `api_client.py`, `db_manager.py`, `main.py`
  - Create `requirements.txt` with `requests`, `mysql-connector-python`, `hypothesis`, `pytest`
  - _Requirements: 1.1, 2.3_

- [x] 2. Implement Database Manager
  - [x] 2.1 Implement `DatabaseManager` class with connection setup and initialization
    - Connect to MySQL at 127.0.0.1:3306 with root/Root@123
    - Create database `probe42_data` if not exists
    - Create `companies` table (id, cin UNIQUE, pan, company_name, created_at, updated_at)
    - Create `error_logs` table (id, error_code, error_message, cin_queried, created_at)
    - _Requirements: 2.3, 5.1, 5.2, 5.3_

  - [x] 2.2 Implement `insert_company` with upsert logic
    - INSERT ON DUPLICATE KEY UPDATE for same CIN
    - _Requirements: 2.2, 2.4_

  - [x] 2.3 Implement `insert_error` method
    - Insert error_code, error_message, cin_queried with auto timestamp
    - _Requirements: 3.1_

- [x] 3. Implement API Client
  - [x] 3.1 Implement `Probe42Client` class
    - Define BASE_URL and API_KEY constants
    - Implement `fetch_company_details(cin)` method
    - Set headers: x-api-key, Accept, x-api-version
    - Return structured response dict with success/error info
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [x] 3.2 Implement error code mapping
    - Map HTTP codes (400, 403, 404, 422, 429, 500, 502, 504) to predefined messages
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9_

- [x] 4. Implement Console App (main.py)
  - [x] 4.1 Implement main loop
    - Initialize DatabaseManager and call initialize()
    - Prompt user for CIN input
    - Call API client, handle success/error
    - On success: extract CIN, PAN, company_name and store in companies table, display to console
    - On error: map error code, store in error_logs table, display to console
    - Loop until user types 'exit' or 'quit'
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 2.2, 3.2-3.9_

- [x] 5. Write all property-based tests
  - [x] 5.1 Write property test: Company data round-trip
    - **Property 1: Company data round-trip**
    - **Validates: Requirements 2.2**

  - [x] 5.2 Write property test: Upsert idempotence
    - **Property 2: Upsert idempotence**
    - **Validates: Requirements 2.4**

  - [x] 5.3 Write property test: Error code mapping correctness
    - **Property 3: Error code mapping correctness**
    - **Validates: Requirements 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9**

  - [x] 5.4 Write property test: Database initialization idempotence
    - **Property 4: Database initialization idempotence**
    - **Validates: Requirements 5.1, 5.2, 5.3**

  - [x] 5.5 Write property test: Error logging round-trip
    - **Property 5: Error logging round-trip**
    - **Validates: Requirements 3.1**

- [x] 6. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All tasks are required
- Property tests use the Hypothesis library with minimum 100 examples
- Database tests require a running MySQL instance at 127.0.0.1:3306
