import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import gzip
from io import BytesIO
import trafilatura
import os
from utils import create_safe_filename
import json

BASE_URL = "https://www.altyortho.com"
PERSIST_DIR = "data/ALTY"
WEB_CONTENT_DIR = os.path.join(PERSIST_DIR, "web_content")

## Function Definitions

def get_sitemap_url(main_site_url):
    robots_url = urljoin(main_site_url, 'robots.txt')
    response = requests.get(robots_url)
    sitemap_exists = False
    if response.status_code == 200:
        sitemap_exists = "sitemap:" in response.text.lower()

    if not sitemap_exists:
        return (False)

    if sitemap_exists:
        lines = response.text.lower().splitlines()
        sitemap_url = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("sitemap:")), None)

    return (sitemap_url)

def crawl_sitemap(sitemap_url):
    if sitemap_url:
        links = []
        sitemaps = [sitemap_url]
        while (len(sitemaps) > 0):
            curr_sitemap = sitemaps.pop(0)
            sitemap_response = requests.get(curr_sitemap)
            if curr_sitemap.endswith(".gz"):
                compressed_file = BytesIO(sitemap_response.content)
                with gzip.open(compressed_file, 'rb') as f:
                    sitemap_parsed = BeautifulSoup(f.read(), features="xml")
            else:
                sitemap_parsed = BeautifulSoup(sitemap_response.content, features="xml")
            curr_site_links_raw = sitemap_parsed.find_all("url")
            if (len(curr_site_links_raw) > 0):
                links = links + [link.find("loc").text for link in curr_site_links_raw]
            curr_site_sitemaps_raw = sitemap_parsed.find_all("sitemap")
            sitemaps = sitemaps + [link.find("loc").text for link in curr_site_sitemaps_raw]
        return (links)
    else:
        print("No sitemap found")
        return (False)

def extract_content(url):
    response = requests.get(url)
    html_content = response.text

    # Extract title using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title Found'

    # Extract main content using Trafilatura
    extracted_content = trafilatura.extract(html_content)

    # Combine Title and Main Content
    if title == 'No Title Found':
        full_content = extracted_content
    else:
        full_content = f"{title}\n{extracted_content}"
    return (full_content)

def extract_and_store_content(url, storage_dir):
    file_name = create_safe_filename(url)
    url_content = extract_content(url)
    storage_path = os.path.join(storage_dir, file_name)
    with open(storage_path, "w") as f:
        f.write(url_content)
    return storage_path

## Main Logic

sitemap_url = get_sitemap_url(BASE_URL)
links = crawl_sitemap(sitemap_url)

if not os.path.exists(PERSIST_DIR):
    os.mkdir(PERSIST_DIR)

if not os.path.exists(WEB_CONTENT_DIR):
    os.mkdir(WEB_CONTENT_DIR)

source_mapping = {}

for link in links:
    source_mapping[extract_and_store_content(link, WEB_CONTENT_DIR)] = link

with open(os.path.join(PERSIST_DIR, "web_content_mapping.json"), "w") as f:
    json.dump(source_mapping, f)