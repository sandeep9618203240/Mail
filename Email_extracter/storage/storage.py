import json
import os

from config import DATA_FILE


def load_existing_ids():

    if not os.path.exists(DATA_FILE):
        return set()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return set()

    emails = data.get("emails", [])

    return {
        email.get("id")
        for email in emails
        if email.get("id")
    }


def save_email(email):

    # Create data folder if it doesn't exist
    os.makedirs(
        os.path.dirname(DATA_FILE),
        exist_ok=True
    )

    # Create new JSON structure if file doesn't exist
    if not os.path.exists(DATA_FILE):

        data = {
            "account": email.get("account"),
            "total_emails": 0,
            "emails": []
        }

    else:

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):

            data = {
                "account": email.get("account"),
                "total_emails": 0,
                "emails": []
            }

    # Check for duplicate
    existing_ids = {
        item.get("id")
        for item in data["emails"]
    }

    if email.get("id") in existing_ids:
        return

    # Add email
    data["emails"].append(email)

    # Update count
    data["total_emails"] = len(data["emails"])

    # Save JSON
    with open(DATA_FILE, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )