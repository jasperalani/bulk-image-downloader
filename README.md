# Bulk Image Downloader

A command line utility that downloads all images from a webpage.

## Features

- Extract images from HTML `<img>` tags and CSS `url()` styles
- Support for custom HTTP headers
- Progress tracking with completion percentage
- Skip existing images (optional re-download with flag)
- Custom download folder location
- Handles relative and absolute URLs

## Installation

### Requirements

- Python 3.6+
- Linux operating system

### Dependencies

Install dependencies using pip:

```bash
pip install requests beautifulsoup4 tqdm
```

## Usage

If using linux download the [latest release](https://github.com/jasperalani/bulk-image-downloader/releases) and use that otherwise clone this project with `git clone github.com/jasperalani/bulk-image-downloader`
- Linux/MacOS:
    ```bash
    bulk_image_downloader https://example.com
    ```
- Windows:
  ```bash
    python bulk_image_downloader.py https://example.com
    ```

### Command Line Arguments

| Argument | Description |
|----------|-------------|
| `website` | Website URL to scrape images from (required) |
| `-f, --folder` | Folder location to download images (default: `./download`) |
| `-r, --redownload` | Redownload images that pre-exist in download folder |
| `-d, --headers` | Custom headers in JSON format |
| `-t, --timeout` | Request timeout in seconds (default: 10) |

### Examples

Download images to default folder:
```bash
python image_downloader.py https://example.com
```

Download to a specific folder:
```bash
python image_downloader.py https://example.com -f ./my_images
```

Force redownload of existing images:
```bash
python image_downloader.py https://example.com -r
```

Use custom headers:
```bash
python image_downloader.py https://example.com -d '{"User-Agent": "Custom Agent", "Referer": "https://example.com"}'
```

Set custom timeout:
```bash
python image_downloader.py https://example.com -t 30
```

## How It Works

1. Fetches the HTML content of the provided website
2. Parses the HTML to extract image URLs from various sources:
   - Standard `<img>` tags
   - Image URLs in srcset attributes
   - Data attributes like data-src, data-lazy, data-original
   - Background images in CSS styles
3. Downloads each image with progress tracking
4. Provides a summary of downloaded, skipped, and failed images

## [License](https://github.com/jasperalani/bulk-image-downloader/blob/main/LICENSE)