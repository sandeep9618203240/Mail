from auth.gmail_auth import get_gmail_service
from scraper import *


def main():

    service = get_gmail_service()

    scrape_emails(service)


if __name__ == "__main__":
    main()