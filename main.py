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
            # Store full response across all tables
            db.store_full_response(cin, result["raw"])
            print("\n--- Company Details ---")
            print(f"  CIN:          {data['cin']}")
            print(f"  PAN:          {data['pan']}")
            print(f"  Company Name: {data['company_name']}")
            print("-" * 30)
            print("All data stored across multiple tables.")

            # Now fetch and store data status
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
