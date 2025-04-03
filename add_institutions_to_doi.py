import requests
import json
import time
import sys
from articles_by_institution import SCOPUS_HEADERS
import os

sys.stdout.reconfigure(encoding='utf-8')
count = 0

api_keys = [
"LIST-YOUR-API-KEYS-HERE"]
api_key_index = 0

SCOPUS_HEADERS["X-ELS-APIKey"] = api_keys[0]


def get_affiliation_to_ref(ref_json_object):
    global count
    global api_key_index
    global api_keys
    doi = ref_json_object["doi"]
    if doi == "N/A":
        return
    url = f"https://api.elsevier.com/content/abstract/doi/{doi}"

    response = requests.get(url, headers=SCOPUS_HEADERS)
    count += 1
    if count % 100 == 0:
        print(f"🔍 {count} requests have been made")

    if response.status_code != 200:
        print(f"❌ API Request Failed: {response.status_code}")
        if response.status_code == 429:
            api_key_index += 1
            if api_key_index >= len(api_keys):
                print("❌ All API Keys have been used")
                sys.exit(1)
                return
            SCOPUS_HEADERS["X-ELS-APIKey"] = api_keys[api_key_index]
            print("🔑 Changing API Key")
            get_affiliation_to_ref(ref_json_object)
            return
        print(response.text)
        return

    data = response.json()
    if "abstracts-retrieval-response" in data and "affiliation" in data["abstracts-retrieval-response"]:
        ref_json_object["affiliation"] = data["abstracts-retrieval-response"]["affiliation"]
    else:
        ref_json_object["affiliation"] = "N/A"

for file in [f"all_articles_by_institution_cited_2014.json"]:#  for year in range(2014, 2019)]:
    if file.endswith(".json"):
        with open(f"data_by_year/{file}", "r", encoding="utf-8") as f:
            data = json.load(f)
            for article in data:
                if "citedby_articles" in article and article["citedby_articles"] != "N/A":
                    for ref in article["citedby_articles"]:
                        get_affiliation_to_ref(ref)
                if "references" in article and article["references"] != "N/A":
                    for ref in article["references"]:
                        get_affiliation_to_ref(ref)
        with open(f"data_by_year/{file}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"{file} has been updated with affiliations")     