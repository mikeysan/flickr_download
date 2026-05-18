# AGENTS.md — Flickr Photo Downloader

## Commands

```bash
uv sync                # Install dependencies
uv run python main.py  # Run (interactive — prompts for download directory)
```

No test suite, linter, formatter, or CI pipeline exists.

## Project Structure

```
main.py          # Entry point — imports and calls flickrdl.main()
flickrdl.py      # All application logic
pyproject.toml   # Project config and dependencies (uv-managed)
uv.lock          # Locked dependency versions
.env             # Credentials (gitignored, must be created manually)
```

## Environment Setup

A `.env` file in the project root is required with:

```
FLICKR_KEY=your_api_key_here
FLICKR_SECRET=your_api_secret_here
FLICKR_USERID=your_user_id_here
```

## Dependencies

| Package | Constraint | Purpose |
|---|---|---|
| `flickrapi` | >=2.4.0 | Flickr API client |
| `requests` | >=2.33.0 | HTTP downloads |
| `python-dotenv` | >=1.2.2 | Load `.env` into environment |
| `icecream` | >=2.1.1 | Debug printing (`ic()`) |

## Architecture Notes

- **Entry point**: `main.py` calls `flickrdl.main()`. All logic lives in `flickrdl.py`.
- **No module-level side effects**: All initialization happens inside `main()`. Safe to import without triggering I/O.
- **Dependency injection**: Core functions accept `flickr` and `download_path` as params.
- **Logging**: `flickrdl.log` at `INFO` level.
- **Rate limiting**: 3600 requests/hour cap (sleeps until next hour) + 2s delay between downloads.

## Style

- Python >=3.12, no type hints, f-strings, `snake_case`
