import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def scrape_job_description(job_url):
    response = requests.get(job_url, headers=HEADERS, timeout=15)

    if response.status_code != 200:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    # SAP job description container
    desc_div = soup.find("div", class_="job-description")

    if not desc_div:
        return ""

    return desc_div.get_text(separator=" ", strip=True)


def enrich_jobs_with_descriptions():
    jobs = pd.read_csv("data/jobs_live.csv")

    descriptions = []

    for i, row in jobs.iterrows():
        print(f"Scraping description {i+1}/{len(jobs)}")
        text = scrape_job_description(row["url"])
        descriptions.append(text)
        time.sleep(2)  # rate limit (IMPORTANT)

    jobs["description"] = descriptions
    jobs.to_csv("data/jobs_raw.csv", index=False)

    print("✅ Job descriptions added → data/jobs_raw.csv")


if __name__ == "__main__":
    enrich_jobs_with_descriptions()
