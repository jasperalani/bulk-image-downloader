# Image Downloader

A simple Python script to download all images from a given webpage.  
Works on **Linux**, **macOS**, and **Windows Subsystem for Linux (WSL)**.

## 😎 Features

- Extract images from HTML `<img>` tags (including srcset) and CSS `url()` styles
- Support for custom HTTP headers
- Progress tracking with completion percentage
- Skip existing images (optional re-download with flag)
- Custom download folder location
- Handles relative and absolute URLs
- Choose a specific image from a `srcset` or fallback to first/last option
<br/><br/>

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/jasperalani/image-downloader.git
cd image-downloader
```

### 2. Install dependencies

First, make sure Python 3 is installed.<br/>

- If using Windows WSL as your linux environment then you might have to create a local python environment:
```bash
python3 -m venv ~/python_custom_env
~/python_custom_env/bin/pip3 install requests beautifulsoup4 tqdm
```
- If using other Linux/Mac:
```bash
pip install requests beautifulsoup4 tqdm
```

### 3. Run the script

- Windows WSL:
```bash
~/python_custom_env/bin/python3 image-downloader.py https://example.com
```
- Linux/Mac:
```bash
python3 image-downloader.py https://example.com
```

Replace `https://example.com` with the URL of the page you want to download images from.
<br/><br/>

## 💿 Command Line Arguments

| Argument | Description |
|----------|-------------|
| `website` | Website URL to scrape images from (required) |
| `-f, --folder` | Folder location to download images (default: `./download`) |
| `-r, --redownload` | Redownload images that pre-exist in download folder |
| `-d, --headers` | Custom headers in JSON format |
| `-t, --timeout` | Request timeout in seconds (default: 10) |
| `-c, --srcset` | Index of image to use from `srcset` (0-based index) |
| `-cf, --srcset-use-first` | Fallback to first image in `srcset` if index is out of range (default: `true`). Set to `false` to fallback to the last image instead. |

### Examples

Download images to default folder:
```bash
image-downloader https://example.com
```

Download to a specific folder:
```bash
image-downloader https://example.com -f ./my_images
```

Force redownload of existing images:
```bash
image-downloader https://example.com -r
```

Use custom headers:
```bash
image-downloader https://example.com -d '{"User-Agent": "Custom Agent", "Referer": "https://example.com"}'
```

Set custom timeout:
```bash
image-downloader https://example.com -t 30
```

Use 4th image from `srcset`, and fallback to **last** image if out of range:
```bash
image-downloader https://example.com -c 4 -cf false
```
<br/>

## [📄 View License](https://github.com/jasperalani/image-downloader/blob/main/LICENSE)
