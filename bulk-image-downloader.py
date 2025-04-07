import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import logging
from tqdm import tqdm

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Bulk Image Downloader")
    parser.add_argument("website", help="Website URL to scrape images from")
    parser.add_argument("-f", "--folder", help="Folder location to download images", default="./download")
    parser.add_argument("-r", "--redownload", help="Redownload images that pre-exist in download folder", action="store_true")
    parser.add_argument("-d", "--headers", help="Custom headers in JSON format", default=None)
    parser.add_argument("-t", "--timeout", help="Request timeout", default=10)
    return parser.parse_args()

def process_headers(args):
    default_headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/107.0.0.0 Safari/537.36')
    }
    custom_headers_print = " using default headers"
    if args.headers:
        try:
            headers = json.loads(args.headers)
            custom_headers_print = " using custom headers"
        except json.JSONDecodeError:
            logging.info("Invalid JSON provided for headers. Using default headers.")
            headers = default_headers
    else:
        headers = default_headers
    return headers, custom_headers_print

def manage_application_folders(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        logging.info(f"Creating sub folder: {path}")
        os.makedirs(path)

def fetch_webpage(url, headers, req_timeout):
    try:
        response = requests.get(url, headers=headers, timeout=req_timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve the website: {e}")
        return None

def extract_image_urls(soup):
    image_urls = set()
    url_pattern = re.compile(r'url\((.*?)\)', re.IGNORECASE)
    
    for img in soup.find_all('img'):
        url = img.get('src')
        if not url:
            srcset = img.get('srcset')
            if srcset:
                srcset_items = [item.strip() for item in srcset.split(',')]
                if srcset_items:
                    url = srcset_items[0].split()[0]
        if not url:
            for attr in ['data-src', 'data-lazy', 'data-original']:
                url = img.get(attr)
                if url:
                    break
        if url:
            image_urls.add(url)
    
    for tag in soup.find_all(style=True):
        style_content = tag['style']
        urls = url_pattern.findall(style_content)
        for url in urls:
            clean_url = url.strip(' "\'')
            if clean_url:
                image_urls.add(clean_url)
                
    return list(image_urls)

def get_save_location(image_url, base_url, sub_folder_path):
    absolute_url = urljoin(base_url, image_url)
    parsed_url = urlparse(absolute_url)
    filename = os.path.basename(parsed_url.path)
    if not filename or '.' not in filename:
        filename = f"image_{hash(absolute_url)}.jpg"
    save_location = os.path.join(sub_folder_path, filename)
    return absolute_url, save_location

def download_image(absolute_url, headers, req_timeout, save_location):
    try:
        img_response = requests.get(absolute_url, headers=headers, timeout=req_timeout)
        img_response.raise_for_status()
        with open(save_location, 'wb') as handler:
            handler.write(img_response.content)
        return True
    except requests.RequestException as e:
        logging.error(f"Failed to download {absolute_url}: {e}")
        return False

def process_images(image_elements, base_url, sub_folder_path, headers, req_timeout, download_preexisting):
    total = len(image_elements)
    downloaded_count = 0
    skipped_count = 0
    failed_count = 0
    
    for i, image_url in enumerate(tqdm(image_elements, desc="Downloading images", unit="image"), start=1):
        percent_complete = round((i - 1) / total * 100)
        absolute_url, save_location = get_save_location(image_url, base_url, sub_folder_path)
        
        if os.path.exists(save_location) and not download_preexisting:
            logging.info(f"{percent_complete}% complete, image already downloaded: {save_location}")
            skipped_count += 1
            continue
        else:
            logging.info(f"{percent_complete}% complete, downloading to {save_location}")
            if download_image(absolute_url, headers, req_timeout, save_location):
                downloaded_count += 1
            else:
                failed_count += 1
    
    return downloaded_count, skipped_count, failed_count

def main():
    args = parse_arguments()
    scrape_url = args.website
    sub_folder_path = args.folder
    download_preexisting = args.redownload
    req_timeout = int(args.timeout)
    
    headers, custom_headers_print = process_headers(args)
    
    if not scrape_url.startswith(('http://', 'https://')):
        scrape_url = 'https://' + scrape_url 
    
    manage_application_folders(sub_folder_path)
    
    logging.info(f"Scraping {scrape_url} for images{custom_headers_print}.")
    html = fetch_webpage(scrape_url, headers, req_timeout)
    if html is None:
        return
    
    soup = BeautifulSoup(html, 'html.parser')
    image_elements = extract_image_urls(soup)
    found_length = len(image_elements)
    if found_length == 0:
        logging.info("No images found.")
        return
    
    logging.info(f"Found {found_length} images.")
    
    downloaded_count, skipped_count, failed_count = process_images(
        image_elements, scrape_url, sub_folder_path, headers, req_timeout, download_preexisting
    )
    
    logging.info("Finished!")
    logging.info(f"Summary: {downloaded_count} downloaded, {skipped_count} skipped, {failed_count} failed.")

if __name__ == "__main__":
    main()
