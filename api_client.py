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
        """
        Fetch comprehensive details for a company by CIN.
        Returns:
            dict with keys:
                success (bool)
                data (dict or None) - contains cin, pan, company_name on success
                error (dict or None) - contains code, message on failure
        """
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
                error_message = get_error_message(response.status_code)
                return {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": response.status_code,
                        "message": error_message,
                    },
                }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": 0,
                    "message": f"Connection error: {str(e)}",
                },
            }

    def fetch_datastatus(self, cin):
        """
        Fetch data status for a company by CIN.
        Returns:
            dict with keys: success, data (data_status dict), error
        """
        url = f"{self.BASE_URL}/{cin}/datastatus"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)

            if response.status_code == 200:
                raw_data = response.json()
                data_status = raw_data.get("data", {}).get("data_status", {})
                return {
                    "success": True,
                    "data": data_status,
                    "error": None,
                }
            else:
                error_message = get_error_message(response.status_code)
                return {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": response.status_code,
                        "message": error_message,
                    },
                }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": 0,
                    "message": f"Connection error: {str(e)}",
                },
            }
