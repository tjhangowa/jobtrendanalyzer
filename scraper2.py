import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- CONFIGURATION ---
# We are targeting the "Back-End Programming" category on We Work Remotely
url = "https://weworkremotely.com/categories/remote-back-end-programming-jobs"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print(f"Fetching jobs from: {url}...")
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Blocked or failed to load page.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# --- THE EXTRACT ---
# On this specific site, jobs are listed inside <section class="jobs">
# and then inside <li> tags.
job_container = soup.find("section", class_="jobs")
job_list = job_container.find_all("li")

data = []
keywords = {"Python": 0, "Java": 0, "Go": 0, "Spring": 0}

print(f"Scanning {len(job_list)} job postings...")

for job in job_list:
    # Some <li> tags are just headers/dividers, so we skip them if they don't have a job class
    # We explicitly look for the 'title' class inside the li
    title_tag = job.find("h3", class_="new-listing__header__title")
    company_tag = job.find("p", class_="new-listing__company-name")

    if title_tag and company_tag:
        title = title_tag.text.strip()
        company = company_tag.text.strip()

        # --- THE ANALYZE (Data Engineering Logic) ---
        # We check if keywords exist in the Title (case insensitive)
        title_lower = title.lower()

        if "python" in title_lower:
            keywords["Python"] += 1
        if "java" in title_lower:
            keywords["Java"] += 1
        if "go" in title_lower:  # Go is another popular backend language
            keywords["Go"] += 1
        if "spring" in title_lower:
            keywords["Spring"] += 1

        data.append({"title": title, "company": company})

# --- THE RESULTS ---
print("\n--- Market Analysis ---")
print(f"Total Jobs Scanned: {len(data)}")
print("Keyword Mentions in Titles:")
for lang, count in keywords.items():
    print(f"{lang}: {count}")

# Save the raw list to CSV so you can look at it
df = pd.DataFrame(data)
df.to_csv("real_jobs.csv", index=False)
print("\nDetailed list saved to 'real_jobs.csv'")