import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. THE SETUP
# This is the URL we want to visit
url = "http://books.toscrape.com/"

# 2. THE EXTRACT (Getting the raw HTML)
print(f"Downloading data from {url}...")
response = requests.get(url)

# Check if it worked (Status 200 is good, 404 is not found, 403 is forbidden)
if response.status_code != 200:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    exit()

# 3. THE TRANSFORM (Parsing the data)
soup = BeautifulSoup(response.text, "html.parser")

# In HTML, books on this site are stored in <article class="product_pod">
books_html = soup.find_all("article", class_="product_pod")

data = []

print(f"Found {len(books_html)} items. Parsing...")

for book in books_html:
    # Extract the Title (it's inside an <h3> tag, then inside an <a> tag)
    title = book.h3.find("a")['title']

    # Extract the Price (it's inside a <p class="price_color">)
    price_text = book.find("p", class_="price_color").text

    # clean the price (remove the weird currency symbol)
    price = float(price_text.replace('Â£', ''))

    # Add to our list
    data.append({"title": title, "price": price})

# 4. THE VISUALIZE (Quick check)
# Convert list to a Pandas DataFrame (like a Table)
df = pd.DataFrame(data)

# Print the top 5 most expensive books on the page
print("\n--- Top 5 Most Expensive Books ---")
print(df.sort_values(by="price", ascending=False).head(5))

# Optional: Save to CSV (Excel)
df.to_csv("market_data.csv", index=False)
print("\nData saved to 'market_data.csv'")