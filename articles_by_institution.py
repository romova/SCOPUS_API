import requests
import json
import time
import sys


sys.stdout.reconfigure(encoding='utf-8')


# Function to get cited references for an article
def get_cited_references(doi):
    if not doi or doi == "N/A":
        return "N/A", []

    url = f"https://api.crossref.org/works/{doi}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to retrieve references for DOI {doi}: {response.status_code}")
            return "N/A", []

        data = response.json()

        authors = [] # This API also gives more info about authors, meanwhile Scopus returns only 1 author
        cited_articles = []

        if "message" in data:
            authors = data["message"].get("author", [])
            authors = [f"{author['family']} {author['given']}" if 'family' in author and 'given' in author else author['name'] if 'name' in author else 'N/A' for author in authors]
            if "reference" in data["message"]:
                references = data["message"]["reference"]
                cited_articles = []   

                for ref in references:
                    cited_articles.append({
                        "title": ref.get("unstructured", "N/A"),
                        "authors": ref.get("author", "N/A"),
                        "doi": ref.get("DOI", "N/A"),
                        "year": ref.get("year", "N/A")
                    })

        return cited_articles, authors

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error retrieving references for DOI {doi}: {e}")

    return "N/A", []


# Function to get articles citing this article (Citing Articles)
def get_citing_articles(scopus_id):
    url = f"https://api.elsevier.com/content/search/scopus?query=REF({scopus_id})"            
    response = requests.get(url, headers=SCOPUS_HEADERS)

    if response.status_code != 200:
        print(f"❌ Failed to retrieve citing articles: {response.status_code}")
        return []

    data = response.json()
    citing_articles = []

    with open("raw_citing_articles.json", "w") as f:
      json.dump(data["search-results"]["entry"], f, indent=4)

    if "search-results" in data and "entry" in data["search-results"]:
        for entry in data["search-results"]["entry"]:
            citing_articles.append({
                "title": entry.get("dc:title", "N/A"),
                "doi": entry.get("prism:doi", "N/A"),
                "year": entry.get("prism:coverDate", "N/A").split("-")[0]
            })
    time.sleep(1)
    return citing_articles




# 🔹 Function to get articles from an institution
def get_articles_by_institution(institution, count=25, start=5025):
    articles = []

    while True:
        print(f"🔄 Fetching articles from index {start}...")

        # 🔹 Construct API URL with pagination
        url = f"https://api.elsevier.com/content/search/scopus?start={start}&count={count}&httpaccept=application/json&query=AFFIL({institution})"

        # 🔹 Make API Request
        response = requests.get(url, headers=SCOPUS_HEADERS)

        if response.status_code != 200:
            print(f"❌ API Request Failed: {response.status_code}")
            print(response.text)
            break # Stop if API request fails
        
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
            cited_by_count = int(entry.get("citedby-count", 0))
            doi = entry.get("prism:doi", "N/A")
            references, authors = get_cited_references(doi)
            if len(authors) == 0:
                authors = entry.get("dc:creator", "N/A")
                if authors != "N/A":
                    authors = [authors]
            batch_articles.append({
                "title": entry.get("dc:title", "N/A"),
                "authors": authors,
                "year": entry.get("prism:coverDate", "N/A").split("-")[0],
                "coverDate": entry.get("prism:coverDate", "N/A"),
                "coverDisplayDate": entry.get("prism:coverDisplayDate", "N/A"),
                "doi": doi,
                "scopus_id": entry.get("dc:identifier", "").replace("SCOPUS_ID:", ""),
                "textType": entry.get("prism:aggregationType", "N/A"),
                "publicationName": entry.get("prism:publicationName", "N/A"),
                "pageRange": entry.get("prism:pageRange", "N/A"),
                "institutions": institutions,
                "affiliation-city": entry.get("affiliation-city", "N/A"),
                "affiliation-country": entry.get("affiliation-country", "N/A"),
                "citedby-count": cited_by_count,
                "citedby_articles": [] if cited_by_count == 0 else get_citing_articles(entry.get("dc:identifier", "").replace("SCOPUS_ID:", "")),
                "references": references
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


#---------------------------------------------------------------------------------------------------------------------


# 🔹 API Key (Replace with yours)
SCOPUS_API_KEY = "API-KEY"

# 🔹 Headers for Scopus API
SCOPUS_HEADERS = {
    "X-ELS-APIKey": SCOPUS_API_KEY,
    "Accept": "application/json"
}

# 🔹 Target Institution
INSTITUTION_NAME = "University of West Bohemia"

# 🔹 Fetch all articles
articles_data = get_articles_by_institution(INSTITUTION_NAME, start=0)

# 🔹 Save results to JSON
file_name = "all_articles_by_institution_cited_5025_.json"
if articles_data:
    with open(file_name, "w") as f:
        json.dump(articles_data, f, indent=4)
    print(f"✅ {len(articles_data)} articles saved to: {file_name}")
else:
    print("❌ No articles found for this institution.")
