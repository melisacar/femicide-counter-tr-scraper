import requests
from bs4 import BeautifulSoup

BASE_URL = "https://anitsayac.com/"
YEAR = 2025

def get_names_and_links(year):
    url = f"{BASE_URL}?year={YEAR}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    names_data = []

    names_spans = soup.find_all("span", class_ = "xxy bgyear2025")

    for span in names_spans:
        link_tag = span.find("a")
        if link_tag:
            name = link_tag.text.strip()
            details_url = BASE_URL + link_tag["href"]
            names_data.append({"name": name, "details_url": details_url})
    return names_data
    
output = get_names_and_links(YEAR)
#print(output)
#print(len(output))