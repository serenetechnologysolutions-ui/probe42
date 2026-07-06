# Requirements Document

## Introduction

A Python-based console application that fetches company comprehensive details from the Probe42 API and stores the data in a MySQL database. The application stores company information (CIN, PAN, company name) in a dedicated table and logs all API error responses in a separate error table.

## Glossary

- **Console_App**: The Python command-line application that orchestrates API calls and database storage
- **API_Client**: The component responsible for making HTTP requests to the Probe42 API
- **Database_Manager**: The component responsible for MySQL database connections and operations
- **Company_Table**: The MySQL table storing company information (CIN, PAN, company name)
- **Error_Table**: The MySQL table storing API error messages
- **CIN**: Corporate Identity Number, a unique identifier for Indian companies (format: U/L + 5 digits + 2 letters + 4 digits + 3 letters + 6 digits)
- **PAN**: Permanent Account Number, a tax identification number

## Requirements

### Requirement 1: API Integration

**User Story:** As a user, I want to fetch company comprehensive details from the Probe42 API, so that I can retrieve and store company data locally.

#### Acceptance Criteria

1. WHEN a user provides a CIN number, THE API_Client SHALL send a GET request to `https://api.probe42.in/probe_pro_sandbox/companies/{CIN}/comprehensive-details` with the correct headers
2. THE API_Client SHALL include the header `x-api-key` with value `Tw7mc8TzlX63z2fP3gul4aBgLWvDmSOu6LDVBDacU18` in every request
3. THE API_Client SHALL include the header `Accept` with value `application/json` in every request
4. THE API_Client SHALL include the header `x-api-version` with value `1.3` in every request
5. WHEN the API returns a successful response (HTTP 200), THE API_Client SHALL parse the JSON response body and return the data

### Requirement 2: Company Data Storage

**User Story:** As a user, I want company information stored in a dedicated MySQL table, so that I can query company details independently.

#### Acceptance Criteria

1. THE Database_Manager SHALL create a Company_Table with columns for CIN number, PAN number, and company name
2. WHEN a successful API response is received, THE Database_Manager SHALL extract the CIN number, PAN number, and company name from the response and insert them into the Company_Table
3. THE Database_Manager SHALL connect to MySQL at host `127.0.0.1`, port `3306`, with username `root` and password `Root@123`
4. IF a company with the same CIN already exists in the Company_Table, THEN THE Database_Manager SHALL update the existing record instead of creating a duplicate

### Requirement 3: Error Logging

**User Story:** As a user, I want all API errors stored in a separate table, so that I can review and troubleshoot failed requests.

#### Acceptance Criteria

1. THE Database_Manager SHALL create an Error_Table with columns for error code, error message, CIN queried, and timestamp
2. WHEN the API returns HTTP 400, THE Console_App SHALL store the error with message "Bad Request - Invalid URL" in the Error_Table
3. WHEN the API returns HTTP 403, THE Console_App SHALL store the error with message "Forbidden - no api-key supplied, incorrect api-key or incorrect URL" in the Error_Table
4. WHEN the API returns HTTP 422, THE Console_App SHALL store the error with message "Validation error - wrong CIN format" in the Error_Table
5. WHEN the API returns HTTP 404, THE Console_App SHALL store the error with message "Resource not found" in the Error_Table
6. WHEN the API returns HTTP 429, THE Console_App SHALL store the error with message "Credits not sufficient" in the Error_Table
7. WHEN the API returns HTTP 500, THE Console_App SHALL store the error with message "Server side error" in the Error_Table
8. WHEN the API returns HTTP 502, THE Console_App SHALL store the error with message "Timeout error - backend system issue" in the Error_Table
9. WHEN the API returns HTTP 504, THE Console_App SHALL store the error with message "AWS gateway timeout" in the Error_Table

### Requirement 4: Console Interface

**User Story:** As a user, I want a simple console interface to input CIN numbers and view results, so that I can interact with the application easily.

#### Acceptance Criteria

1. WHEN the application starts, THE Console_App SHALL prompt the user to enter a CIN number
2. WHEN a successful response is received, THE Console_App SHALL display the company name, CIN, and PAN to the console
3. WHEN an error response is received, THE Console_App SHALL display the error code and message to the console
4. WHEN a query completes, THE Console_App SHALL prompt the user to enter another CIN or exit the application

### Requirement 5: Database Initialization

**User Story:** As a user, I want the database and tables created automatically, so that I do not need to manually set up the schema.

#### Acceptance Criteria

1. WHEN the application starts, THE Database_Manager SHALL create the database if it does not already exist
2. WHEN the application starts, THE Database_Manager SHALL create the Company_Table if it does not already exist
3. WHEN the application starts, THE Database_Manager SHALL create the Error_Table if it does not already exist
