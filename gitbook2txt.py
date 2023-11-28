import requests
from bs4 import BeautifulSoup
import os
import sys

# Check if the command line argument (GitBook URL) is provided
if len(sys.argv) != 2:
    print("Usage: python gitbook2txt.py [GitBook URL]")
    sys.exit(1)

gitbook_url = sys.argv[1]

# Function to download a single page
def download_page(url, folder):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text content
        text = soup.get_text()

        # Format the filename
        title = soup.title.string.split('|')[0].strip().replace(' ', '_').replace('/', '_')
        filename = f"{folder}/{title}.txt"

        # Save the file in text format
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
            print(f"Downloaded: {filename}")

    except Exception as e:
        print(f"Error downloading page {url}: {e}")

# Main function to download the entire Gitbook
def download_gitbook(main_url):
    try:
        response = requests.get(main_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Create a directory for the GitBook
        book_title = soup.title.string.split('|')[0].strip().replace(' ', '_').replace('/', '_')
        folder = f"GitBook_{book_title}"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Find all links in the GitBook
        links = soup.find_all('a')
        page_urls = set()

        for link in links:
            href = link.get('href')
            if href and not href.startswith('http'):
                full_url = requests.compat.urljoin(main_url, href)
                page_urls.add(full_url)

        # Download each page
        for url in page_urls:
            download_page(url, folder)

    except Exception as e:
        print(f"Error downloading GitBook: {e}")

# Run the script with the provided GitBook URL
download_gitbook(gitbook_url)
