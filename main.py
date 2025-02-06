import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://anitsayac.com/"

def get_names_and_links(year):
    url = f"{BASE_URL}?year={year}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    names_data = []

    # Set the class name depending on the year
    if year == 2025:
        class_name = "xxy bgyear2025"
    else:
        class_name = "xxy"  # For all years other than 2025

    # Getting the names of the victims and the links to their detail pages
    names_spans = soup.find_all("span", class_=class_name)

    for span in names_spans:
        link_tag = span.find("a")
        if link_tag:
            name = link_tag.text.strip()
            details_url = BASE_URL + link_tag["href"]
            names_data.append({"name": name, "details_url": details_url})
    return names_data

def get_details(details_url):
    response = requests.get(details_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    details = {}

    # Finding all <b> tags on the page
    b_tags = soup.find_all("b")

    for b_tag in b_tags:
        # Getting the text after each <b> tag
        label = b_tag.text.strip()

        # Getting the text and tags after the label
        next_node = b_tag.find_next_sibling(text=True)
        if next_node:
            value = next_node.strip()
        else:
            # If there is no text, there may be other tags containing text
            value = b_tag.find_next_sibling().get_text(strip=True) if b_tag.find_next_sibling() else "No information"
        label = label.replace(":", "")  # Removing ':' character

        # If the value is empty, we set it as "No information"
        if not value:
            value = "No information"

        details[label] = value

    # Getting the source information (if available)
    source_tag = soup.find("a", href=True)
    if source_tag:
        details["Kaynak"] = source_tag["href"]

    return details

# Fetching the data for both 2024 and 2025
for year in [2024, 2025]:
    print(f"Fetching data for {year}...")
    victims = get_names_and_links(year)

    # Fetching details for each victim
    for victim in victims:
        print(f"\nFetching details for: {victim['name']} at {victim['details_url']}")
        details = get_details(victim["details_url"])  # Fetch the details
        victim.update(details)  # Add the details to the main data

        # Printing all the details
        for key, value in details.items():
            print(f"{key}: {value}")
        print("="*50)  # Adding a separator line
        #time.sleep(1)  # Wait for one second per request
