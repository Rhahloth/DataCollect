import os, sys, json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy.inspection import inspect
from db import db
from config import GOOGLE_SHEET_ID

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def get_gspread_client():
    """
    Get an authorized gspread client.
    - On Render: uses GOOGLE_CREDENTIALS env var (full JSON string).
    - On Desktop/EXE: falls back to credentials.json file.
    """
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    if creds_json:
        try:
            creds_dict = json.loads(creds_json)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            print("Google credentials loaded from environment variable")
        except Exception as e:
            raise RuntimeError(f"Failed to load GOOGLE_CREDENTIALS from env: {e}")
    else:
        # Local fallback for dev or EXE builds
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
        cred_path = os.path.join(base_path, "credentials.json")

        if not os.path.exists(cred_path):
            raise FileNotFoundError("No GOOGLE_CREDENTIALS env var and no credentials.json file found")

        creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
        print("DEBUG: GOOGLE_CREDENTIALS exists?", bool(os.getenv("GOOGLE_CREDENTIALS")))

    return gspread.authorize(creds)


def sync_to_sheets(model_instance, sheet_name, exclude_fields=None):
    """
    Sync a SQLAlchemy record to Google Sheets.
    Ensures headers exist, skips duplicates by record id.
    """
    if exclude_fields is None:
        exclude_fields = ["created_at", "updated_at", "synced"]

    try:
        mapper = inspect(model_instance.__class__)
        columns = [c.key for c in mapper.columns if c.key not in exclude_fields]

        client = get_gspread_client()
        sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)

        # Ensure headers
        existing_headers = sheet.row_values(1)
        if not existing_headers:
            sheet.insert_row(columns, 1)

        # Build row (stringified values to match Google Sheets)
        row = []
        for col in columns:
            val = getattr(model_instance, col)
            if col == "synced":
                row.append("TRUE" if val else "FALSE")
            elif val is None:
                row.append("")
            elif hasattr(val, "isoformat"):
                row.append(val.isoformat())
            else:
                row.append(str(val))

        # Check for duplicates by ID (assumes 'id' is in columns)
        record_id = str(getattr(model_instance, "id", None))
        if record_id:
            all_ids = sheet.col_values(columns.index("id") + 1)  # +1 because Sheets cols are 1-based
            if record_id in all_ids:
                print(f"Skipping duplicate for {model_instance.__class__.__name__} id={record_id}")
                return "already"

        # Append row
        sheet.append_row(row, value_input_option="USER_ENTERED")
        return True

    except Exception as e:
        print(f"Error syncing {model_instance.__class__.__name__} to {sheet_name}: {e}")
        return False


