import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_sap_jobs(keyword="ai", pages=1):
    jobs = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    for start in range(0, pages * 25, 25):
        url = f"https://jobs.sap.com/search/?q={keyword}&startrow={start}"
        response = requests.get(url, headers=headers, timeout=15)

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("tr.data-row")

        for row in rows:
            title = row.select_one("a.jobTitle-link")
            location = row.select_one("span.jobLocation")

            if title and location:
                jobs.append({
                    "title": title.get_text(strip=True),
                    "location": location.get_text(strip=True),
                    "url": "https://jobs.sap.com" + title["href"]
                })

    if not jobs:
        return 0

    os.makedirs("data", exist_ok=True)
    with open("data/jobs_live.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        writer.writeheader()
        writer.writerows(jobs)

    return len(jobs)
