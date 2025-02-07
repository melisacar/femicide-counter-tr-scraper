import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
import re  
import time 

BASE_URL = "https://anitsayac.com/"

def sanitize_text(text):
    if not isinstance(text, str):  
        text = str(text)  
    return re.sub(r'[\x00-\x1F\x7F]', '', text)

def get_names_and_links(year):
    url = f"{BASE_URL}?year={year}"
    response = requests.get(url, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    names_data = []

    class_name = "xxy bgyear2025" if year == 2025 else "xxy"
    #class_name = "xxy"

    names_spans = soup.find_all("span", class_=class_name)

    for span in names_spans:
        link_tag = span.find("a")
        if link_tag:
            name = sanitize_text(link_tag.text.strip())  
            details_url = BASE_URL + link_tag["href"]
            names_data.append({"Isim": name, "Detay URL": details_url})
    return names_data

def get_details(details_url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

    response = requests.get(details_url, headers=headers, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    details = {}

    b_tags = soup.find_all("b")

    for b_tag in b_tags:
        label = sanitize_text(b_tag.get_text(strip=True)) if b_tag else ""
        next_node = b_tag.find_next_sibling(string=True) if b_tag.find_next_sibling() else ""

        if next_node:
            value = sanitize_text(next_node.strip())  
        else:
            value = sanitize_text(b_tag.find_next_sibling().get_text(strip=True)) if b_tag.find_next_sibling() else "No information"
        
        label = label.replace(":", "")

        if not value:
            value = "No information"

        details[label] = value

    source_tag = soup.find("a", href=True)
    details["Kaynak"] = source_tag["href"] if source_tag else "No information"

    time.sleep(5)

    return details

def fetch_and_save_data():
    all_victims_data = []

    for year in [2024]:
        victims = get_names_and_links(year)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(get_details, victim["Detay URL"]): victim for victim in victims}

            for future in concurrent.futures.as_completed(futures):
                victim = futures[future]
                try:
                    details = future.result()
                    victim.update(details)

                    victim = {key: sanitize_text(value) for key, value in victim.items()}
                    all_victims_data.append(victim)

                except Exception as e:
                    print(f"Error: {victim['Detay URL']} - {e}")

        print(f"{year} is done.")

    df = pd.DataFrame(all_victims_data)

    excel_filename = "femicide_data_2025_to_2008.xlsx"
    df.to_excel(excel_filename, index=False, engine="openpyxl")

    print(f"Saved to {excel_filename}.")

fetch_and_save_data()
