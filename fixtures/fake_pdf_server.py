"""
Task 3 fixture: a local stand-in for the policy site with a deliberate fault.

The index page links to three "policy documents":

    /policy/valid.pdf      a real (minimal) PDF served as application/pdf
    /policy/not-a-pdf.pdf  an HTML error page served as text/html with 200 OK
    /policy/corrupt.pdf    starts with %PDF but is truncated (no %%EOF)

The second and third links reproduce Task 2 scenario 5 (T009 and T010):
a link that looks like a PDF but is not a usable PDF file. A correct scraper
should report both as failed downloads. The Task 1 prototype reports all
three as "Downloaded successfully", because it only checks the status code.

Usage (from the repository root):

    python3 fixtures/fake_pdf_server.py            # serves on http://localhost:3000
    uv run --with-requirements requirements.txt scraper.py http://localhost:3000/policy/

Stop the server with Ctrl+C. Only the Python standard library is used.
"""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

INDEX_HTML = b"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Policy library (test fixture)</title></head>
<body>
  <h1>Policy library</h1>
  <ul>
    <li><a href="valid.pdf">Valid policy</a></li>
    <li><a href="not-a-pdf.pdf">Policy that is really an HTML page</a></li>
    <li><a href="corrupt.pdf">Policy with a corrupt PDF</a></li>
  </ul>
</body>
</html>
"""

# Smallest well-formed PDF: one empty page, correct xref offsets, %%EOF trailer.
VALID_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
    b"xref\n0 4\n"
    b"0000000000 65535 f \n"
    b"0000000009 00000 n \n"
    b"0000000052 00000 n \n"
    b"0000000101 00000 n \n"
    b"trailer<</Size 4/Root 1 0 R>>\n"
    b"startxref\n164\n%%EOF\n"
)

NOT_A_PDF = b"""<!DOCTYPE html>
<html><head><title>Document unavailable</title></head>
<body><p>Sorry, this document is temporarily unavailable.</p></body></html>
"""

# Starts with the PDF signature but is cut off part-way through the first object.
CORRUPT_PDF = VALID_PDF[:40]

ROUTES = {
    "/policy/": (200, "text/html; charset=utf-8", INDEX_HTML),
    "/policy/valid.pdf": (200, "application/pdf", VALID_PDF),
    "/policy/not-a-pdf.pdf": (200, "text/html; charset=utf-8", NOT_A_PDF),
    "/policy/corrupt.pdf": (200, "application/pdf", CORRUPT_PDF),
}


class FixtureHandler(BaseHTTPRequestHandler):
    """Serves the fixed routes above; anything else is 404."""

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/policy"):
            path = "/policy/"
        status, content_type, body = ROUTES.get(
            path, (404, "text/plain; charset=utf-8", b"Not found\n")
        )
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_server(port=3000):
    """Create (but do not start) the fixture server. Used by the tests."""
    return ThreadingHTTPServer(("127.0.0.1", port), FixtureHandler)


def main():
    parser = argparse.ArgumentParser(description="Faulty policy-site fixture (Task 3).")
    parser.add_argument("--port", type=int, default=3000)
    args = parser.parse_args()
    server = make_server(args.port)
    print(f"Serving fixture on http://localhost:{args.port}/policy/ (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
