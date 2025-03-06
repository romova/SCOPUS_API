import requests
import json
import time

# 🔹 API Key (Replace with yours)
SCOPUS_API_KEY = "5642da61c2650be9daf95f821c5d6536"

# 🔹 Headers for Scopus API
SCOPUS_HEADERS = {
    "X-ELS-APIKey": SCOPUS_API_KEY,
    "Accept": "application/json"
}

# 🔹 Target Institution
# INSTITUTION_NAME = "University of West Bohemia"
INSTITUTION_NAME = "NTIS"

# 🔹 Function to get articles from an institution
def get_articles_by_institution(institution, count=25, start=0):
    articles = []

    while True:
        print(f"🔄 Fetching articles from index {start}...")
        
        # 🔹 Construct API URL with pagination
        url = f"https://api.elsevier.com/content/search/scopus?start={start}&count={count}&httpaccept=application/json&query=AFFIL({institution})"
        
        # 🔹 Make API Request
        response = requests.get(url, headers=SCOPUS_HEADERS)

        if response.status_code != 200:
            print(f"❌ API Request Failed: {response.status_code}")
            break  # Stop if API request fails

        data = response.json()

        # 🔹 Check if results exist
        if "search-results" not in data or "entry" not in data["search-results"]:
            print("✅ No more articles found.")
            break  # Stop if no more articles are returned

        # 🔹 Process each article
        batch_articles = []
        for entry in data["search-results"]["entry"]:
            institutions = []

            # 🔹 Extract institutions per article (if available)
            if "affiliation" in entry and isinstance(entry["affiliation"], list):
                institutions = [aff.get("affilname", "Unknown Institution") for aff in entry["affiliation"]]

            # 🔹 Append article data
            batch_articles.append({
                "title": entry.get("dc:title", "N/A"),
                "doi": entry.get("prism:doi", "N/A"),
                "authors": entry.get("dc:creator", "N/A"),
                "year": entry.get("prism:coverDate", "N/A").split("-")[0],
                "journal": entry.get("prism:publicationName", "N/A"),
                "scopus_id": entry.get("dc:identifier", "").replace("SCOPUS_ID:", ""),
                "theme": entry.get("prism:aggregationType", "N/A"),
                "institutions": institutions
            })

        # 🔹 Add batch to full articles list
        articles.extend(batch_articles)

        # 🔹 Stop if fewer articles than count were returned (last batch)
        if len(batch_articles) < count:
            print("✅ All available articles have been retrieved.")
            break

        # 🔹 Move to the next batch
        start += count

        # 🔹 Optional: Avoid hitting API rate limits
        time.sleep(1)  # Delay to prevent excessive requests

    return articles

# 🔹 Fetch all articles
articles_data = get_articles_by_institution(INSTITUTION_NAME)

# 🔹 Save results to JSON
file_name = "all_articles_by_institution1.json"
if articles_data:
    with open(file_name, "w") as f:
        json.dump(articles_data, f, indent=4)
    print(f"✅ {len(articles_data)} articles saved to: {file_name}")
else:
    print("❌ No articles found for this institution.")
