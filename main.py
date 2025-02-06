import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://anitsayac.com/"
YEAR = 2025

def get_names_and_links(year):
    url = f"{BASE_URL}?year={YEAR}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    names_data = []

    names_spans = soup.find_all("span", class_="xxy bgyear2025")

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

    print(f"Page content for {details_url}:\n")
    print(soup.prettify())  

    details = {}
    detail_rows = soup.find_all("tr")

    for row in detail_rows:
        columns = row.find_all("td")
        if len(columns) == 2:
            key = columns[0].text.strip().replace(":", "")
            value = columns[1].text.strip()
            details[key] = value
    return details

victims = get_names_and_links(YEAR)

for victim in victims:
    print(f"\nFetching details for: {victim['name']} at {victim['details_url']}")
    details = get_details(victim["details_url"])  
    victim.update(details)  

    # Tüm detayları yazdır
    for key, value in details.items():
        print(f"{key}: {value}")
    print("="*50)  
    time.sleep(1)  
