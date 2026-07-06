"""
Property-based tests for Probe42 Company Data Console.
Uses Hypothesis for property-based testing.
Requires a running MySQL instance at 127.0.0.1:3306.
"""
import pytest
from hypothesis import given, settings, assume
from hypothesis.strategies import text, sampled_from, integers
import string

from db_manager import DatabaseManager
from api_client import get_error_message, ERROR_CODE_MAP


# --- Strategies ---

def cin_strategy():
    """Generate valid CIN-like strings (21 chars, alphanumeric)."""
    return text(
        alphabet=string.ascii_uppercase + string.digits,
        min_size=21,
        max_size=21,
    )


def pan_strategy():
    """Generate valid PAN-like strings (10 chars, alphanumeric)."""
    return text(
        alphabet=string.ascii_uppercase + string.digits,
        min_size=10,
        max_size=10,
    )


def company_name_strategy():
    """Generate non-empty company name strings."""
    return text(
        alphabet=string.ascii_letters + string.digits + " .-&",
        min_size=1,
        max_size=100,
    )


# --- Fixtures ---

@pytest.fixture(scope="module")
def db():
    """Provide a DatabaseManager connected to a test database."""
    manager = DatabaseManager()
    manager.DB_NAME = "probe42_test"
    manager.initialize()
    yield manager
    # Cleanup
    cursor = manager.connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS probe42_test")
    cursor.close()
    manager.close()


@pytest.fixture(autouse=True)
def clean_tables(db):
    """Clean tables before each test."""
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM companies")
    cursor.execute("DELETE FROM error_logs")
    db.connection.commit()
    cursor.close()


# --- Property 1: Company data round-trip ---
# Feature: probe42-company-data, Property 1: Company data round-trip
# For any valid company data (CIN, PAN, company name), inserting then querying
# by CIN should return the same PAN and company name.
# Validates: Requirements 2.2

@settings(max_examples=100)
@given(cin=cin_strategy(), pan=pan_strategy(), name=company_name_strategy())
def test_company_data_round_trip(db, cin, pan, name):
    """Property 1: Inserting company data and querying returns the same values."""
    # Clean before each hypothesis example
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM companies")
    db.connection.commit()
    cursor.close()

    db.insert_company(cin, pan, name)
    result = db.get_company_by_cin(cin)

    assert result is not None
    assert result["cin"] == cin
    assert result["pan"] == pan
    assert result["company_name"] == name


# --- Property 2: Upsert idempotence ---
# Feature: probe42-company-data, Property 2: Upsert idempotence
# For any CIN and two different sets of (PAN, name), inserting both with the same CIN
# should result in exactly one record containing the second set's values.
# Validates: Requirements 2.4

@settings(max_examples=100)
@given(
    cin=cin_strategy(),
    pan1=pan_strategy(),
    name1=company_name_strategy(),
    pan2=pan_strategy(),
    name2=company_name_strategy(),
)
def test_upsert_idempotence(db, cin, pan1, name1, pan2, name2):
    """Property 2: Inserting same CIN twice results in one record with latest values."""
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM companies")
    db.connection.commit()
    cursor.close()

    db.insert_company(cin, pan1, name1)
    db.insert_company(cin, pan2, name2)

    count = db.get_company_count_by_cin(cin)
    assert count == 1

    result = db.get_company_by_cin(cin)
    assert result["pan"] == pan2
    assert result["company_name"] == name2


# --- Property 3: Error code mapping correctness ---
# Feature: probe42-company-data, Property 3: Error code mapping correctness
# For any known HTTP error code from {400, 403, 404, 422, 429, 500, 502, 504},
# the mapping function should return the corresponding predefined message.
# Validates: Requirements 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9

KNOWN_CODES = list(ERROR_CODE_MAP.keys())


@settings(max_examples=100)
@given(code=sampled_from(KNOWN_CODES))
def test_error_code_mapping_correctness(code):
    """Property 3: Known error codes map to their predefined messages."""
    message = get_error_message(code)
    expected = ERROR_CODE_MAP[code]
    assert message == expected


# --- Property 4: Database initialization idempotence ---
# Feature: probe42-company-data, Property 4: Database initialization idempotence
# For any number of consecutive calls to initialize(), the database and tables
# should exist and no errors should be raised.
# Validates: Requirements 5.1, 5.2, 5.3

@settings(max_examples=100)
@given(n=integers(min_value=1, max_value=5))
def test_database_initialization_idempotence(n):
    """Property 4: Calling initialize() N times is equivalent to calling it once."""
    manager = DatabaseManager()
    manager.DB_NAME = "probe42_test_init"
    try:
        for _ in range(n):
            manager.initialize()
        # Verify tables exist by running queries
        cursor = manager.connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'companies'")
        assert cursor.fetchone() is not None
        cursor.execute("SHOW TABLES LIKE 'error_logs'")
        assert cursor.fetchone() is not None
        cursor.close()
    finally:
        cursor = manager.connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS probe42_test_init")
        cursor.close()
        manager.close()


# --- Property 5: Error logging round-trip ---
# Feature: probe42-company-data, Property 5: Error logging round-trip
# For any error code, error message, and CIN string, inserting an error log entry
# and querying the most recent entry for that CIN should return the same values.
# Validates: Requirements 3.1

@settings(max_examples=100)
@given(
    code=sampled_from(KNOWN_CODES),
    cin=cin_strategy(),
)
def test_error_logging_round_trip(db, code, cin):
    """Property 5: Inserting an error and querying returns the same values."""
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM error_logs")
    db.connection.commit()
    cursor.close()

    message = ERROR_CODE_MAP[code]
    db.insert_error(code, message, cin)

    result = db.get_latest_error_by_cin(cin)
    assert result is not None
    assert result["error_code"] == code
    assert result["error_message"] == message
    assert result["cin_queried"] == cin
