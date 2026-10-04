import base64

from config import ACCOUNT_NAME


def decode_body(data):

    if not data:
        return ""

    try:
        decoded_bytes = base64.urlsafe_b64decode(data)
        return decoded_bytes.decode("utf-8", errors="replace")

    except Exception:
        return ""


def parse_email(message):

    payload = message.get("payload", {})

    # -------------------------
    # Extract headers
    # -------------------------

    headers = payload.get("headers", [])

    sender = ""
    receiver = ""
    subject = ""
    date = ""

    for header in headers:

        name = header.get("name", "").lower()
        value = header.get("value", "")

        if name == "from":
            sender = value

        elif name == "to":
            receiver = value

        elif name == "subject":
            subject = value

        elif name == "date":
            date = value

    # -------------------------
    # Extract body
    # -------------------------

    body = ""

    parts = payload.get("parts", [])

    for part in parts:

        if part.get("mimeType") == "text/plain":

            body_data = part.get(
                "body", {}
            ).get("data", "")

            body = decode_body(body_data)

            break

    # -------------------------
    # Create email object
    # -------------------------

    email = {
        "id": message.get("id"),
        "thread_id": message.get("threadId"),

        "account": ACCOUNT_NAME,

        "sender": sender,
        "receiver": receiver,
        "subject": subject,
        "date": date,

        "body": body,

        "gmail_labels": message.get(
            "labelIds", []
        )
    }

    return email