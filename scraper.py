#!/usr/bin/env python3
"""
CITS5501 Project Phase 2 -- starter code for the Task 1 minimal prototype.

What this starter already does:

- reads an optional start URL from the command line (defaults to the
  policy index page),
- fetches that page via `fetch()`, which sets a timeout and a User-Agent,
  waits briefly between requests, and stops the program if it would exceed
  MAX_REQUESTS,
- extracts every <a href="..."> link on the page and makes it absolute,
- prints the links it found.

What you need to write (look for "TODO"):

- `is_policy_link()`: decide which links look like policy documents,
- `describe_download()`: download one document and print its metadata,
- the loop at the end of `main()` that picks 3-5 distinct documents
  and calls `describe_download()` on each.

Run with:

    uv run --with-requirements requirements.txt scraper.py
    uv run --with-requirements requirements.txt scraper.py http://localhost:3000/

(See README.md for other ways to run it.)
"""

import argparse
import sys
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

START_URL = "https://uwa-policy.cits5501.arranstewart.io/policy/"

# Politeness and safety limits. Please don't raise these when running
# against the live site.
MAX_REQUESTS = 20       # total requests per run (index page + downloads)
TIMEOUT_SECONDS = 10    # per request; `requests` has NO timeout by default
DELAY_SECONDS = 1.0     # pause between consecutive requests

# You may want to add your team number here
USER_AGENT = "CITS5501-student-scraper/0.1 (university course project)"

class RequestLimitExceeded(Exception):
    """Raised when a run tries to make more than MAX_REQUESTS requests."""

# keep track of how many request we have made.
_request_count = 0


def fetch(session, url, **kwargs):
    """
    Make a GET request, enforcing the request cap, a timeout and a delay.

    Use this for every request your prototype makes, rather than calling
    `session.get()` directly. Any extra keyword arguments (e.g. `stream=True`)
    are passed through to `session.get()`.

    Returns a `requests.Response`. Note that this does NOT raise an exception
    for 4xx/5xx status codes -- check `response.status_code` yourself.
    """

    global _request_count
    if _request_count >= MAX_REQUESTS:
        raise RequestLimitExceeded(
            f"request limit of {MAX_REQUESTS} reached; not fetching {url}"
        )
    if _request_count > 0:
        time.sleep(DELAY_SECONDS)
    _request_count += 1

    kwargs.setdefault("timeout", TIMEOUT_SECONDS)
    return session.get(url, **kwargs)


def extract_links(html, base_url):
    """
    Return a list of absolute URLs for every <a href="..."> in `html`,
    in the order they appear. Relative links are resolved against `base_url`.
    Duplicates are NOT removed.
    """
    soup = BeautifulSoup(html, "html.parser")
    return [urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True)]


def is_policy_link(url):
    """
    Return True if `url` looks like it leads to a downloadable policy
    document (e.g. a PDF or office file), otherwise False.

    TODO: implement this. Filtering by file extension is acceptable for
    the prototype -- but note its limitations in your report.
    """
    path = urlparse(url).path.lower()
    extensions = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".rtf", ".odt")

    return path.endswith(extensions)

def describe_download(session, url):
    """
    Download the document at `url` and print its metadata: for example the
    URL, HTTP status, declared content type, downloaded size, and
    (optionally) the first few bytes of the response body.

    The downloaded data does not need to be saved to disk.

    TODO: implement this, using `fetch()` to make the request.
    """
    response = fetch(session, url)
    data = response.content

    print("\nPolicy URL:", url)
    print("HTTP status:", response.status_code)
    print("Content type:", response.headers.get("Content-Type", "Unknown"))
    print("Downloaded size:", len(data), "bytes")
    print("Initial bytes:", repr(data[:10]))

    if response.status_code == 200:
        print("Downloaded successfully")
    else:
        print("Download failed")


def main():
    """
    main routine
    """

    parser = argparse.ArgumentParser(
        description="Minimal policy-document scraper prototype (CITS5501)."
    )
    parser.add_argument(
        "start_url",
        nargs="?",
        default=START_URL,
        help=f"index page to start from (default: {START_URL})",
    )
    args = parser.parse_args()

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    print(f"Fetching index page: {args.start_url}")
    response = fetch(session, args.start_url)
    print(f"  status: {response.status_code}, "
          f"content type: {response.headers.get('Content-Type')}")

    links = extract_links(response.text, response.url)
    print(f"Found {len(links)} links:")
    for link in links:
        print(f"  {link}")

    policy_links = [link for link in links if is_policy_link(link)]
    print(f"{len(policy_links)} of these look like policy documents.")

    # TODO: choose 3-5 *distinct* policy links and call describe_download()
    # on each. Keep within MAX_REQUESTS (the index page already used one).
    selected_links = []
    start_hostname = urlparse(args.start_url).hostname

    for link in policy_links:
        parsed_link = urlparse(link)

        if parsed_link.hostname != start_hostname:
            continue

        link = parsed_link._replace(fragment="").geturl()

        if link not in selected_links:
            selected_links.append(link)

        if len(selected_links) == 3:
            break

    for link in selected_links:
        describe_download(session, link)

    print(f"Requests made: {_request_count} (limit {MAX_REQUESTS})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
