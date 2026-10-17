"""
Task 3 demonstration test (T009/T010): documents that look like PDFs but are not.

Runs the Task 1 scraper's describe_download() against the local fixture server
and checks that a non-PDF or corrupt "PDF" is not reported as a successful
download. Against the Task 1 prototype, the valid-PDF test passes and the other two
tests FAIL, which is the failure this fixture is designed to expose.

Run from the repository root:

    uv run --with-requirements requirements.txt --with pytest pytest tests/
"""

import threading

import pytest
import requests
from fake_pdf_server import make_server

import scraper


@pytest.fixture(scope="module")
def base_url():
    server = make_server(port=0)  # port 0: pick any free port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}/policy/"
    server.shutdown()
    server.server_close()


@pytest.fixture(autouse=True)
def no_delay(monkeypatch):
    # Keep the tests fast and independent of the request counter.
    monkeypatch.setattr(scraper, "DELAY_SECONDS", 0)
    monkeypatch.setattr(scraper, "_request_count", 0)


def download_report(url, capsys):
    session = requests.Session()
    session.trust_env = False  # never route localhost through a proxy
    scraper.describe_download(session, url)
    return capsys.readouterr().out


def test_valid_pdf_is_reported_as_success(base_url, capsys):
    out = download_report(base_url + "valid.pdf", capsys)
    assert "Downloaded successfully" in out


def test_html_served_as_pdf_is_not_a_success(base_url, capsys):
    out = download_report(base_url + "not-a-pdf.pdf", capsys)
    assert "Downloaded successfully" not in out, (
        "an HTML page (Content-Type text/html) was reported as a downloaded PDF"
    )


def test_corrupt_pdf_is_not_a_success(base_url, capsys):
    out = download_report(base_url + "corrupt.pdf", capsys)
    assert "Downloaded successfully" not in out, (
        "a truncated PDF with no %%EOF marker was reported as a downloaded PDF"
    )
