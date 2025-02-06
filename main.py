import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures

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
            names_data.append({"Isim": name, "Detay URL": details_url})
    return names_data

def get_details(details_url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

    response = requests.get(details_url, headers=headers)

    #response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    details = {}

    # Finding all <b> tags on the page
    b_tags = soup.find_all("b")

    for b_tag in b_tags:
        label = b_tag.string.strip() if b_tag.string else ""
        next_node = b_tag.find_next_sibling(text=True) if b_tag.find_next_sibling() else ""

        if next_node:
            value = next_node.strip()
        else:
            value = b_tag.find_next_sibling().get_text(strip=True) if b_tag.find_next_sibling() else "No information"
        label = label.replace(":", "")  # Removing ':' character

        if not value:
            value = "No information"

        details[label] = value

    # Getting the source information (if available)
    source_tag = soup.find("a", href=True)
    if source_tag:
        details["Kaynak"] = source_tag["href"]

    return details

def fetch_and_save_data():
    all_victims_data = []

    # Fetching the data for both 2025 and 2024
    for year in range(2025, 2007, -1):
        victims = get_names_and_links(year)

        # Using ThreadPoolExecutor to fetch details in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Fetching details for each victim concurrently
            futures = [executor.submit(get_details, victim["Detay URL"]) for victim in victims]

            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                victim = victims[i]
                details = future.result()  # Fetch the details
                victim.update(details)  # Add the details to the main data
                victim['Yıl'] = year  # Add the year to the data
                all_victims_data.append(victim)  # Store the victim's data in the list
        print(f"Year {year} is done.")

    # Convert to DataFrame
    df = pd.DataFrame(all_victims_data)

    # Save to Excel
    excel_filename = "femicide_data_2025_to_2008.xlsx"
    df.to_excel(excel_filename, index=False, engine="openpyxl")

    print(f"Data saved to {excel_filename}")

# Run the function
fetch_and_save_data()
