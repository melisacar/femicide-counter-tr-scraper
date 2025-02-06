# Femicide Counter (Türkiye)

This project scrapes data from the [AnitSayac](https://anitsayac.com/) website and saves it into an Excel file. Users can access the data for a specific year and gather detailed information about each data entry. The data collection process is implemented in Python, and parallel processing is used to speed up the data retrieval.

## Requirements

To run this project, the following Python libraries are required:

- requests: To make HTTP requests
- BeautifulSoup: For HTML parsing
- pandas: To process and save the data into an Excel file
- concurrent.futures: For parallel processing
- re: For using regular expressions (regex) to clean text

You can install the necessary libraries using the following command:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## How It Works

The scraper fetches data from AnıtSayac by:

1. Scraping a list of names and corresponding detail URLs for a specific year.
2. For each name, it scrapes detailed information available at the corresponding detail URL.
3. The gathered data is then cleaned (removing unwanted characters) and stored in an Excel file.

## How to Run

1. Clone this repository to your local machine.
2. Install the necessary dependencies by running the command mentioned above.
3. Run the `fetch_and_save_data()` function in the script to start collecting the data.
4. The script will save the scraped data into an Excel file.

## Notes

- Make sure to run this script responsibly, as frequent requests to the website may result in being temporarily blocked. If you encounter issues, such as a "403 Forbidden" error, you may need to use a proxy service.
- The script uses parallel processing (`ThreadPoolExecutor`) to speed up data retrieval.