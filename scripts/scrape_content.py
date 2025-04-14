import requests
import json
import os
import sys
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Any, Optional

# --- Configuration ---
STRUCTURE_FILE_PATH: str = "data/structure.json"
OUTPUT_DATA_DIR: str = "data"
BASE_URL: str = "https://modelcontextprotocol.io" # Used to resolve relative links if needed, though structure.json should have full URLs now
REQUEST_HEADERS: Dict[str, str] = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
REQUEST_TIMEOUT: int = 15 # seconds

# --- Helper Functions ---

def fetch_and_parse(url: str) -> Optional[BeautifulSoup]:
    """Fetches HTML from a URL and parses it with BeautifulSoup."""
    print(f"Fetching: {url}", file=sys.stderr)
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        print(f"  Status: {response.status_code}", file=sys.stderr)
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error parsing {url}: {e}", file=sys.stderr)
        return None

def extract_content_html(soup: BeautifulSoup) -> Optional[str]:
    """Extracts the main content HTML from the parsed page."""
    content_area = soup.find('div', id='content-area')
    if not content_area or not isinstance(content_area, Tag):
        print("  Error: Could not find main content area 'div#content-area'.", file=sys.stderr)
        return None

    # Try finding the primary prose container first
    main_prose = content_area.find('div', class_=lambda x: x and 'relative' in x and 'mt-8' in x and 'prose' in x)
    if main_prose and isinstance(main_prose, Tag):
        print("  Found primary prose container.", file=sys.stderr)
        return str(main_prose) # Return the HTML content of this div

    # Fallback: If specific prose div isn't found, maybe return the whole content-area?
    # Or look for other common patterns. For now, let's stick to the specific div.
    print("  Warning: Could not find specific 'div.relative.mt-8.prose' container within #content-area.", file=sys.stderr)
    # Let's try returning the whole content_area as a fallback, might need refinement
    # return str(content_area)
    return None # Or return None if the specific div is required

def convert_to_markdown(html_content: str) -> str:
    """Converts HTML content to Markdown."""
    # Configure markdownify options if needed (e.g., heading style, code language handling)
    # See https://github.com/matthewwithanm/python-markdownify for options
    md = markdownify(html_content, heading_style="ATX")
    return md

def get_save_path(url: str, base_output_dir: str) -> Optional[str]:
    """Determines the local file path based on the URL."""
    try:
        parsed_url = urlparse(url)
        path_segments = [seg for seg in parsed_url.path.split('/') if seg]

        if not path_segments:
            # Handle root path, e.g., https://modelcontextprotocol.io/
            # Decide on a filename, maybe 'index.md' or based on title if available
            # For now, let's assume structure.json won't link directly to the root
            # or handle it based on a known title like 'Introduction'
            if url == BASE_URL or url == BASE_URL + '/':
                 # Let's map the base URL to introduction.md as a convention
                 return os.path.join(base_output_dir, "introduction.md")
            else:
                 print(f"  Warning: Cannot determine path for URL with no segments: {url}", file=sys.stderr)
                 return None


        # If the last segment looks like a filename (has an extension), use it directly
        # Otherwise, assume it's a directory and append 'index.md' or use the segment as filename.md
        # Let's use the segment as filename.md for simplicity, matching common static site generators
        filename = path_segments[-1] + ".md"
        dir_path = os.path.join(base_output_dir, *path_segments[:-1])

        return os.path.join(dir_path, filename)

    except Exception as e:
        print(f"Error determining save path for {url}: {e}", file=sys.stderr)
        return None

def save_markdown(file_path: str, markdown_content: str) -> None:
    """Saves the Markdown content to the specified file path, creating directories if needed."""
    try:
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"  Saved: {file_path}", file=sys.stderr)
    except IOError as e:
        print(f"Error writing file {file_path}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error saving {file_path}: {e}", file=sys.stderr)

def process_structure_item(item: Dict[str, Any], base_output_dir: str) -> None:
    """Processes a single item (page or group) from the structure."""
    if "path" in item and isinstance(item["path"], str):
        url = item["path"]
        title = item.get("title", "Unknown Title")
        print(f"Processing '{title}': {url}", file=sys.stderr)

        soup = fetch_and_parse(url)
        if not soup:
            return

        content_html = extract_content_html(soup)
        if not content_html:
            print(f"  No content extracted for {url}", file=sys.stderr)
            return

        markdown_content = convert_to_markdown(content_html)
        if not markdown_content:
            print(f"  Markdown conversion failed for {url}", file=sys.stderr)
            return

        save_path = get_save_path(url, base_output_dir)
        if not save_path:
            print(f"  Could not determine save path for {url}", file=sys.stderr)
            return

        save_markdown(save_path, markdown_content)

    # Recursively process children if this item is a group
    if "children" in item and isinstance(item["children"], list):
        print(f"Processing children of '{item.get('title', 'Unnamed Group')}'...", file=sys.stderr)
        for child_item in item["children"]:
            process_structure_item(child_item, base_output_dir)

# --- Main Execution ---

def main() -> None:
    """Main function to load structure and process all items."""
    print("Starting content scraping process...", file=sys.stderr)
    try:
        with open(STRUCTURE_FILE_PATH, 'r', encoding='utf-8') as f:
            structure_data = json.load(f)
        print(f"Loaded structure from {STRUCTURE_FILE_PATH}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: Structure file not found at {STRUCTURE_FILE_PATH}", file=sys.stderr)
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {STRUCTURE_FILE_PATH}: {e}", file=sys.stderr)
        return
    except Exception as e:
        print(f"Error loading {STRUCTURE_FILE_PATH}: {e}", file=sys.stderr)
        return

    if not isinstance(structure_data, list):
        print("Error: Structure data is not a list.", file=sys.stderr)
        return

    # Ensure base output directory exists
    try:
        os.makedirs(OUTPUT_DATA_DIR, exist_ok=True)
    except OSError as e:
        print(f"Error creating base output directory {OUTPUT_DATA_DIR}: {e}", file=sys.stderr)
        return

    print(f"Processing {len(structure_data)} top-level items...", file=sys.stderr)
    for item in structure_data:
        process_structure_item(item, OUTPUT_DATA_DIR)

    print("Content scraping process finished.", file=sys.stderr)

if __name__ == "__main__":
    main()
