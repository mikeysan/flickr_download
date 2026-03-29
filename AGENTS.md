# AGENTS.md — Flickr Photo Downloader

## Project Overview

A single-file Python script (`flickrdl.py`) that downloads all photos from a Flickr user account at original resolution. It uses the Flickr API with authenticated credentials stored in a `.env` file. MIT licensed, authored by Michael Mba.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script (interactive — prompts for download directory)
python flickrdl.py
```

There is no build step, test suite, linter config, or CI pipeline in this repository.

## Project Structure

```
flickrdl.py        # Entire application — all logic in one file
requirements.txt   # Pinned Python dependencies
.env               # Credentials (gitignored, must be created manually)
README.md
LICENSE
```

## Environment Setup

A `.env` file in the project root is required with three variables:

```
FLICKR_KEY=your_api_key_here
FLICKR_SECRET=your_api_secret_here
FLICKR_USERID=your_user_id_here
```

The script reads these at startup via `python-dotenv` and will fail with `None`-related errors if they are missing.

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `flickrapi` | 2.4.0 | Flickr API client |
| `requests` | 2.33.0 | HTTP downloads |
| `python-dotenv` | 0.19.0 | Load `.env` into environment |
| `icecream` | 2.1.1 | Debug printing (`ic()`) |

## Code Patterns & Architecture

- **Single-file design**: Everything lives in `flickrdl.py`. No modules, classes, or packages.
- **Module-level side effects**: The Flickr API client and `download_path` are initialized at module scope (lines 15–36), not inside `main()`. This means importing the module triggers user input via `input()`.
- **Logging**: Uses Python's `logging` module to `flickr_downloader.log` at `INFO` level.
- **Debug output**: Uses `icecream` (`ic()`) for ad-hoc debug printing in `create_normalized_directory()`.
- **Error handling**: `download_photo()` catches `RequestException` and generic `Exception` separately. Other functions catch generic `Exception`.
- **Rate limiting**: `main()` enforces a 3600-request-per-hour limit (sleeps until the next hour) and a 2-second delay between individual downloads.

## Known Issues & Gotchas

- **`download_photo` signature mismatch**: `download_photo(photo_id)` is defined with one parameter (line 39), but `main()` calls it with two arguments — `download_photo(photo['id'], sizes)` (line 119). This is a runtime bug that will cause a `TypeError`.
- **Script name discrepancy**: README says to run `python flickr_downloader.py` but the actual file is `flickrdl.py`.
- **Module-level I/O**: `create_normalized_directory()` is called at import time (line 36), so importing the module in a REPL or test will block on `input()`.
- **Hardcoded `.jpg` extension**: All photos are saved as `.jpg` regardless of actual format (e.g., PNG, GIF uploads to Flickr).
- **Log filename**: The log file is `flickr_downloader.log`, which differs from the script name.
- **No pagination guard**: If `get_photos` returns `None`, `main()` returns without incrementing the page — this could cause an infinite loop in some edge cases (though the `No photos found.` early return usually prevents it).

## Style Conventions

- Python 3, no type hints
- f-strings for string formatting throughout
- `snake_case` function naming
- No tests, no linter config, no formatter config
- Bare `except Exception` used for broad error handling
