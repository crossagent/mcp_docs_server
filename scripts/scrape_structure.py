import requests
import json
import sys
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional, Any

def extract_structure(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    Extracts the navigation structure from the parsed HTML.

    Args:
        soup: BeautifulSoup object representing the parsed HTML.

    Returns:
        A list of dictionaries representing the navigation structure.
    """
    structure: List[Dict[str, Any]] = []
    nav_items_div = soup.find('div', id='navigation-items')

    if not nav_items_div or not isinstance(nav_items_div, Tag):
        print("Debug: Error - Could not find navigation items container 'div#navigation-items'.", file=sys.stderr)
        return []
    else:
        print("Debug: Found navigation items container 'div#navigation-items'.", file=sys.stderr)

    # Find all group containers directly under nav_items_div
    # These seem to be divs with a class like 'mt-12' or 'mt-8'
    group_divs = nav_items_div.find_all('div', recursive=False)
    print(f"Debug: Found {len(group_divs)} potential group divs.", file=sys.stderr)

    for group_div in group_divs:
        # Find the group title (h5) within this div
        h5 = group_div.find('h5', recursive=False)
        if not h5:
            # Skip divs that don't represent a navigation group (like the SDK links div)
            print(f"Debug: Skipping div without h5 title.", file=sys.stderr)
            continue

        group_title = h5.get_text(strip=True)
        print(f"Debug: Processing group: {group_title}", file=sys.stderr)
        current_group: Dict[str, Any] = {"title": group_title, "children": []}

        # Find the list (ul) within this group div
        ul = group_div.find('ul', recursive=False)
        if not ul:
            print(f"Debug: No ul found in group: {group_title}", file=sys.stderr)
            continue

        # Find all list items (li) within this ul
        list_items = ul.find_all('li', recursive=False)
        print(f"Debug: Found {len(list_items)} list items in group: {group_title}", file=sys.stderr)

        for li in list_items:
            link = li.find('a', href=True)
            div_toggle = li.find('div', class_='flex-1') # Check for expandable groups like Quickstart

            if link:
                title = link.get_text(strip=True)
                path = link['href']
                item = {"title": title, "path": path}
                current_group["children"].append(item)
                print(f"Debug: Added item: {title} ({path})", file=sys.stderr)
            elif div_toggle:
                 # Handle expandable groups like Quickstart - needs manual mapping for now
                 title = div_toggle.get_text(strip=True)
                 if title == "Quickstart":
                     print(f"Debug: Handling special case: {title}", file=sys.stderr)
                     quickstart_group = {"title": title, "children": [
                         {"title": "For Server Developers", "path": "/quickstart/server"},
                         {"title": "For Client Developers", "path": "/quickstart/client"},
                         {"title": "For Claude Desktop Users", "path": "/quickstart/user"}
                     ]}
                     current_group["children"].append(quickstart_group)
                 else:
                     print(f"Debug: Found unhandled div toggle: {title}", file=sys.stderr)
            else:
                print(f"Debug: Skipping li element without link or known toggle: {li.prettify()}", file=sys.stderr)

        if current_group["children"]:
             structure.append(current_group)
        else:
            print(f"Debug: Group '{group_title}' has no children, not adding.", file=sys.stderr)


    print(f"Debug: Final extracted structure (before return): {structure}", file=sys.stderr)
    return structure

def main() -> None:
    """
    Main function to fetch, parse, and print the navigation structure.
    """
    url: str = "https://modelcontextprotocol.io/introduction" # Any page with the sidebar works
    headers: Dict[str, str] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    print(f"Debug: Attempting to fetch URL: {url}", file=sys.stderr)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Debug: Received response with status code: {response.status_code}", file=sys.stderr)
        response.raise_for_status() # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}", file=sys.stderr)
        return

    try:
        print("Debug: Parsing HTML content with BeautifulSoup...", file=sys.stderr)
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Debug: HTML parsed successfully.", file=sys.stderr)
        print("Debug: Calling extract_structure...", file=sys.stderr)
        doc_structure = extract_structure(soup)
        print(f"Debug: extract_structure returned: {doc_structure}", file=sys.stderr)

        if doc_structure:
            output_path = "data/structure.json"
            print(f"Debug: Structure found, attempting to write JSON to {output_path}...", file=sys.stderr)
            try:
                # Write the JSON structure directly to the file with UTF-8 encoding
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(doc_structure, f, indent=2, ensure_ascii=False)
                print(f"Debug: JSON successfully written to {output_path}.", file=sys.stderr)
            except IOError as e:
                print(f"Error writing JSON to file {output_path}: {e}", file=sys.stderr)
        else:
            print("Debug: No structure extracted or structure is empty. Not writing file.", file=sys.stderr)

    except Exception as e:
        print(f"Error during processing: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
