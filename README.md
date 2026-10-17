# CITS5501/CITS3501 Group Project – Policy Scraper Prototype

Group project repository for CITS5501/CITS3501 Software Testing and Quality Assurance, Semester 2 2026.

`scraper.py` is a minimal prototype (Phase 2, Task 1) that starts from the
[UWA policy index page](https://uwa-policy.cits5501.arranstewart.io/policy/),
finds links that look like policy documents, downloads three distinct documents
and prints their metadata. Downloaded data is discarded; nothing is written to disk.

## Repository contents

| Path | Description |
| --- | --- |
| `scraper.py` | Task 1 prototype scraper |
| `requirements.txt` | Python dependencies (`requests`, `beautifulsoup4`) |
| `.python-version` | Python version used by uv (3.12) |
| `.devcontainer/` | Development container (Ubuntu 22.04, Python, uv, OpenJDK 21, Git) |

## Requirements

- [uv](https://docs.astral.sh/uv/) (recommended), or Python 3.11+ with `pip`
- Network access to `https://uwa-policy.cits5501.arranstewart.io`

uv downloads a suitable Python version and the dependencies automatically on first run.

## Running the prototype

From the repository root:

```bash
uv run --with-requirements requirements.txt scraper.py
```

To start from a different index page, such as a local copy of the site used for testing:

```bash
uv run --with-requirements requirements.txt scraper.py http://localhost:3000/
```

### Without uv

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 scraper.py
```

## Output

The scraper prints:

1. the index page URL, HTTP status and content type;
2. every link found on the index page, and how many look like policy documents;
3. for each of the three documents downloaded: the policy URL, HTTP status,
   declared `Content-Type`, downloaded size in bytes and the first 10 bytes of the body
   (`%PDF` indicates a PDF, `PK` an Office Open XML file such as `.docx`);
4. the total number of requests made.

Example (run against a local test copy of the site):

```text
Policy URL: http://localhost:3000/policy/a.pdf
HTTP status: 200
Content type: application/pdf
Downloaded size: 13 bytes
Initial bytes: b'%PDF-1.4 f'
Downloaded successfully
...
Requests made: 4 (limit 20)
```

## Request limits

All requests go through `fetch()`, which applies a 10-second timeout, sends a
User-Agent header, waits 1 second between requests and stops after 20 requests.
These limits should be kept when running against the live site.

## Known limitations

The prototype is deliberately minimal. In particular, it treats any `200 OK`
response as a successful download, identifies documents by file extension only,
and does not handle timeouts or connection errors. See the Phase 2 report
(Task 1) for the full list of limitations and assumptions.

## Development environment

The marking environment is Ubuntu 22.04 (x86-64) with `python3`, `uv` and
`openjdk-21-jdk`. To develop in a matching environment:

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and check it works:
   ```bash
   docker --version
   docker run hello-world
   ```
   (On Windows, install WSL if prompted, then restart.)
2. In VS Code, install the **Dev Containers** and **Container Tools** extensions (Microsoft).
3. Open the repository and run **Dev Containers: Reopen in Container** (`Ctrl+Shift+P`).
   The terminal should open in `/workspace`.
4. Check the toolchain:
   ```bash
   python3 --version   # Python 3.10.12
   uv --version
   javac --version     # javac 21
   git --version
   ```
