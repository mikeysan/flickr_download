# AGENTS.md — Flickr Photo Downloader

## Project Overview

A Python script that downloads all photos from a Flickr user account at original resolution. Uses the Flickr API with authenticated credentials stored in a `.env` file. MIT licensed, authored by Michael Mba.

## Commands

```bash
# Install dependencies
uv sync

# Run the script (interactive — prompts for download directory)
uv run python main.py
```

There is no test suite, linter config, or CI pipeline in this repository.

## Project Structure

```
main.py             # Entry point — imports and calls flickrdl.main()
flickrdl.py         # All application logic
pyproject.toml      # Project config and dependencies (uv-managed)
uv.lock             # Locked dependency versions
requirements.txt    # Legacy pinned dependencies (superseded by pyproject.toml)
.env                # Credentials (gitignored, must be created manually)
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

The script reads these at startup via `python-dotenv` inside `main()`. Missing values will cause `None`-related errors from the Flickr API.

## Dependencies

| Package | Constraint | Purpose |
|---|---|---|
| `flickrapi` | >=2.4.0 | Flickr API client |
| `requests` | >=2.33.0 | HTTP downloads |
| `python-dotenv` | >=0.19.0 | Load `.env` into environment |
| `icecream` | >=2.1.1 | Debug printing (`ic()`) |

## Code Patterns & Architecture

- **Entry point**: `main.py` imports and calls `flickrdl.main()`. All logic lives in `flickrdl.py`.
- **No module-level side effects**: All initialization (dotenv loading, Flickr client creation, logging config, directory prompt) happens inside `flickrdl.main()`. The module is safe to import without triggering I/O.
- **Dependency injection**: Core functions accept `flickr` and `download_path` as parameters rather than relying on module globals.
- **Logging**: Uses Python's `logging` module to `flickrdl.log` at `INFO` level.
- **Debug output**: Uses `icecream` (`ic()`) for ad-hoc debug printing in `create_normalized_directory()`.
- **Error handling**: `download_photo()` catches `RequestException` and generic `Exception` separately. Other functions catch generic `Exception`.
- **Rate limiting**: `main()` enforces a 3600-request-per-hour limit (sleeps until the next hour) and a 2-second delay between individual downloads.
- **File extensions**: Photo file extensions are derived from the download URL rather than hardcoded.

## Style Conventions

- Python 3 (>=3.12), no type hints
- f-strings for string formatting throughout
- `snake_case` function naming
- No tests, no linter config, no formatter config
- Bare `except Exception` used for broad error handling
