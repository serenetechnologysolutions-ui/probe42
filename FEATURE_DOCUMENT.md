# Feature Document: Probe42 Company Data Console

## Overview

A Python-based console application that fetches company comprehensive details and data status from the Probe42 API and stores all information in a normalized MySQL database across multiple tables.

## APIs Used

| # | API Endpoint | Purpose |
|---|-------------|---------|
| 1 | `GET /companies/{CIN}/comprehensive-details` | Fetches full company data (financials, directors, GST, legal, etc.) |
| 2 | `GET /companies/{CIN}/datastatus` | Fetches data freshness/status metadata |

**Base URL:** `https://api.probe42.in/probe_pro_sandbox/companies`  
**API Key:** `x5I00Ry4bU7pPZsKDu7JE227W6ZV1SRTsjHARt87`  
**Headers:** `x-api-key`, `Accept: application/json`, `x-api-version: 1.3`

## Database Configuration

- **Host:** 127.0.0.1
- **Port:** 3306
- **Username:** root
- **Password:** Root@123
- **Database:** probe42_data

## Database Schema (20 Tables)

| # | Table Name | Source | Description |
|---|-----------|--------|-------------|
| 1 | `companies` | data.company | Core company info (CIN, PAN, name, address, status) |
| 2 | `directors` | data.authorized_signatories | Directors/signatories with DIN, designation, dates |
| 3 | `financials` | data.financials | Parent financial record (year, nature, filing type) |
| 4 | `financial_ratios` | data.financials[].ratios | 16 financial ratios per year |
| 5 | `financial_balance_sheet` | data.financials[].bs | Assets, liabilities, subtotals |
| 6 | `financial_pnl` | data.financials[].pnl.lineItems | P&L line items and subtotals |
| 7 | `financial_cash_flow` | data.financials[].cash_flow | All cash flow statement items |
| 8 | `financial_pnl_key_schedule` | data.financials[].pnl_key_schedule | Managerial remuneration, auditor fees, insurance, power |
| 9 | `financial_auditor` | data.financials[].auditor | Auditor name, firm, PAN, adverse remarks |
| 10 | `financial_revenue_breakup` | data.financials[].pnl.revenue_breakup + depreciation_breakup | Revenue sources and depreciation split |
| 11 | `financial_parameters` | data.financial_parameters | CSR, FC earnings, employees, gross assets |
| 12 | `shareholdings` | data.shareholdings | Shareholding pattern by year/category |
| 13 | `gst_details` | data.gst_details | GSTIN registrations across states |
| 14 | `legal_history` | data.legal_history | Court cases (petitioner, respondent, status) |
| 15 | `charges` | data.open_charges | Secured lending charges |
| 16 | `contact_details` | data.contact_details | Emails and phone numbers |
| 17 | `epfo_establishments` | data.establishments_registered_with_epfo | EPFO registrations |
| 18 | `credit_ratings` | data.credit_ratings | Credit ratings from agencies |
| 19 | `related_party_transactions` | data.related_party_transactions | RPT by financial year and party type |
| 20 | `data_status` | datastatus API | Data freshness (last updated dates) |
| 21 | `error_logs` | Error responses | API error logging |

## Application Flow

```
User enters CIN
    → API 1: comprehensive-details
        → Store in 19 tables (companies, directors, financials, etc.)
    → API 2: datastatus
        → Store in data_status table
    → Display results to console
    → Loop (or exit)
```

## Error Handling

| HTTP Code | Message |
|-----------|---------|
| 400 | Bad Request - Invalid URL |
| 403 | Forbidden - no api-key supplied, incorrect api-key or incorrect URL |
| 404 | Resource not found |
| 422 | Validation error - wrong CIN format |
| 429 | Credits not sufficient |
| 500 | Server side error |
| 502 | Timeout error - backend system issue |
| 504 | AWS gateway timeout |

All errors are logged to the `error_logs` table with timestamp.

## Project Files

| File | Purpose |
|------|---------|
| `main.py` | Console application entry point |
| `api_client.py` | Probe42 API client (comprehensive-details + datastatus) |
| `db_manager.py` | MySQL database manager (schema + storage methods) |
| `requirements.txt` | Python dependencies |
| `test_properties.py` | Property-based tests (Hypothesis) |

## Dependencies

```
requests==2.31.0
mysql-connector-python==8.3.0
hypothesis==6.98.0
pytest==8.0.0
```

## How to Run

```bash
pip install -r requirements.txt
python3 main.py
```

---

## Source Code

### main.py

```python
from api_client import Probe42Client
from db_manager import DatabaseManager


def main():
    print("=" * 50)
    print("  Probe42 Company Data Console")
    print("=" * 50)

    db = DatabaseManager()
    try:
        db.initialize()
        print("Database initialized successfully.\n")
    except Exception as e:
        print(f"Database connection failed: {e}")
        return

    client = Probe42Client()

    while True:
        cin = input("Enter CIN number (or 'exit' to quit): ").strip()

        if cin.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not cin:
            print("Please enter a valid CIN number.\n")
            continue

        print(f"Fetching details for CIN: {cin}...")
        result = client.fetch_company_details(cin)

        if result["success"]:
            data = result["data"]
            db.store_full_response(cin, result["raw"])
            print("\n--- Company Details ---")
            print(f"  CIN:          {data['cin']}")
            print(f"  PAN:          {data['pan']}")
            print(f"  Company Name: {data['company_name']}")
            print("-" * 30)
            print("All data stored across multiple tables.")

            print("Fetching data status...")
            ds_result = client.fetch_datastatus(cin)
            if ds_result["success"]:
                db.store_datastatus(cin, ds_result["data"])
                print("  Data status stored.")
                ds = ds_result["data"]
                print(f"  Last updated: {ds.get('last_details_updated', 'N/A')}")
                print(f"  Last FY end:  {ds.get('last_fin_year_end', 'N/A')}")
            else:
                err = ds_result["error"]
                db.insert_error(err["code"], err["message"], cin)
                print(f"  [ERROR {err['code']}] {err['message']}")
            print()
        else:
            error = result["error"]
            db.insert_error(error["code"], error["message"], cin)
            print(f"\n[ERROR {error['code']}] {error['message']}")
            print("Error logged to database.\n")

    db.close()


if __name__ == "__main__":
    main()
```

### api_client.py

```python
import requests


ERROR_CODE_MAP = {
    400: "Bad Request - Invalid URL",
    403: "Forbidden - no api-key supplied, incorrect api-key or incorrect URL",
    422: "Validation error - wrong CIN format",
    404: "Resource not found",
    429: "Credits not sufficient",
    500: "Server side error",
    502: "Timeout error - backend system issue",
    504: "AWS gateway timeout",
}


def get_error_message(code):
    """Map an HTTP error code to its predefined message."""
    return ERROR_CODE_MAP.get(code, f"Unknown error (HTTP {code})")


class Probe42Client:
    BASE_URL = "https://api.probe42.in/probe_pro_sandbox/companies"
    API_KEY = "x5I00Ry4bU7pPZsKDu7JE227W6ZV1SRTsjHARt87"

    def __init__(self):
        self.headers = {
            "x-api-key": self.API_KEY,
            "Accept": "application/json",
            "x-api-version": "1.3",
        }

    def fetch_company_details(self, cin):
        """Fetch comprehensive details for a company by CIN."""
        url = f"{self.BASE_URL}/{cin}/comprehensive-details"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            if response.status_code == 200:
                raw_data = response.json()
                company = raw_data.get("data", {}).get("company", {})
                return {
                    "success": True,
                    "data": {
                        "cin": company.get("cin", cin),
                        "pan": company.get("pan", ""),
                        "company_name": company.get("legal_name", ""),
                    },
                    "raw": raw_data,
                    "error": None,
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "error": {"code": response.status_code, "message": get_error_message(response.status_code)},
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": {"code": 0, "message": f"Connection error: {str(e)}"}}

    def fetch_datastatus(self, cin):
        """Fetch data status for a company by CIN."""
        url = f"{self.BASE_URL}/{cin}/datastatus"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            if response.status_code == 200:
                raw_data = response.json()
                data_status = raw_data.get("data", {}).get("data_status", {})
                return {"success": True, "data": data_status, "error": None}
            else:
                return {
                    "success": False,
                    "data": None,
                    "error": {"code": response.status_code, "message": get_error_message(response.status_code)},
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": {"code": 0, "message": f"Connection error: {str(e)}"}}
```

### db_manager.py

```python
import mysql.connector


class DatabaseManager:
    DB_NAME = "probe42_data"

    def __init__(self, host="127.0.0.1", port=3306, user="root", password="Root@123"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None

    def _get_connection(self, database=None):
        config = {"host": self.host, "port": self.port, "user": self.user, "password": self.password}
        if database:
            config["database"] = database
        return mysql.connector.connect(**config)

    def initialize(self):
        """Creates database and all 21 tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.DB_NAME}")
        cursor.close()
        conn.close()

        self.connection = self._get_connection(database=self.DB_NAME)
        cursor = self.connection.cursor()

        # Tables: companies, directors, financials, financial_ratios,
        # financial_balance_sheet, financial_pnl, financial_cash_flow,
        # financial_pnl_key_schedule, financial_auditor, financial_revenue_breakup,
        # financial_parameters, shareholdings, gst_details, legal_history,
        # charges, contact_details, epfo_establishments, credit_ratings,
        # related_party_transactions, data_status, error_logs
        # (See db_manager.py for full CREATE TABLE statements)
        ...

    def store_full_response(self, cin, data):
        """Store comprehensive-details response across all tables."""
        ...

    def store_datastatus(self, cin, data_status):
        """Store datastatus API response."""
        ...

    def insert_error(self, error_code, error_message, cin_queried):
        """Log an API error."""
        ...

    def close(self):
        """Close database connection."""
        ...
```

*(Full implementation in `db_manager.py` file - 900+ lines with all table creation and storage methods)*

---

## Sample Output

```
==================================================
  Probe42 Company Data Console
==================================================
Database initialized successfully.

Enter CIN number (or 'exit' to quit): U15549PN1992FTC065522
Fetching details for CIN: U15549PN1992FTC065522...

--- Company Details ---
  CIN:          U15549PN1992FTC065522
  PAN:          AAACB8573G
  Company Name: COCA COLA INDIA PRIVATE LIMITED
------------------------------
All data stored across multiple tables.
Fetching data status...
  Data status stored.
  Last updated: 2026-05-16
  Last FY end:  2025-03-31
```

## Data Stored Per Company

| Table | Typical Rows | Notes |
|-------|-------------|-------|
| companies | 1 | Upsert on CIN |
| directors | 25 | All current + past |
| financials | 24 | One per FY |
| financial_ratios | 24 | One per FY |
| financial_balance_sheet | 24 | One per FY |
| financial_pnl | 24 | One per FY |
| financial_cash_flow | 24 | One per FY |
| financial_pnl_key_schedule | 24 | One per FY |
| financial_auditor | 22 | One per FY (where available) |
| financial_revenue_breakup | 24 | One per FY |
| financial_parameters | 12 | One per FY (recent years) |
| shareholdings | 4 | By category/year |
| gst_details | 18 | Multiple state registrations |
| legal_history | 211 | All court cases |
| contact_details | 1 | Emails + phones |
| epfo_establishments | 2 | PF registrations |
| related_party_transactions | 294 | By FY and party |
| data_status | 1 | Upsert on CIN |
| error_logs | varies | Append-only |
