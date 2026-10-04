import time

from googleapiclient.errors import HttpError

from config import MAX_RESULTS
from gmail.parser import parse_email
from storage.storage import load_existing_ids, save_email


def scrape_emails(service):

    # Load emails that are already stored
    existing_ids = load_existing_ids()

    print(f"Already stored: {len(existing_ids)} emails")

    page_token = None
    new_emails = 0
    skipped_emails = 0

    while True:

        try:

            # Get a page of Gmail message IDs
            results = service.users().messages().list(
                userId="me",
                maxResults=MAX_RESULTS,
                pageToken=page_token
            ).execute()

        except HttpError as error:

            print("Gmail API error:", error)

            print("Waiting 10 seconds before retrying...")
            time.sleep(10)

            continue

        messages = results.get("messages", [])

        print(f"\nFound {len(messages)} emails in this page.")

        # Process each email
        for message in messages:

            msg_id = message["id"]

            # Skip emails that are already stored
            if msg_id in existing_ids:

                skipped_emails += 1
                continue

            try:

                # Get complete Gmail message
                gmail_message = service.users().messages().get(
                    userId="me",
                    id=msg_id,
                    format="full"
                ).execute()

                # Convert Gmail message into our format
                email = parse_email(gmail_message)

                # Save email
                save_email(email)

                # Remember this ID
                existing_ids.add(msg_id)

                new_emails += 1

                if new_emails % 10 == 0:
                    print(
                        f"New emails saved: {new_emails}"
                    )

                # Small delay to reduce API rate-limit problems
                time.sleep(0.5)

            except HttpError as error:

                print(
                    f"Error fetching email {msg_id}:",
                    error
                )

                print("Waiting 10 seconds...")
                time.sleep(10)

                continue

        # Get next page
        page_token = results.get("nextPageToken")

        # No more pages
        if not page_token:
            break

    print("\n==============================")
    print("SCRAPING COMPLETED")
    print("==============================")

    print(f"Previously stored : {skipped_emails}")
    print(f"New emails        : {new_emails}")
    print(f"Total stored      : {len(existing_ids)}")