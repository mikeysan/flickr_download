# Flickr Photo Downloader

Download all photos from a Flickr account at original resolution.

## Prerequisites

- Python >=3.12
- Flickr API key and secret ([get one here](https://www.flickr.com/services/apps/create/))

## Setup

```bash
git clone https://github.com/mikeysan/flickr_download.git
cd flickr_download
uv sync
```

Create a `.env` file in the project root:

```
FLICKR_KEY=your_api_key_here
FLICKR_SECRET=your_api_secret_here
FLICKR_USERID=your_user_id_here
```

## Usage

```bash
uv run python main.py
```

The script prompts for a download directory, then downloads all photos from the configured account at original resolution. Progress and errors are logged to `flickrdl.log`.

## License

MIT — see [LICENSE](LICENSE).
