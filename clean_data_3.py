# removes diacritics
import unicodedata
import sys
import os
import json

sys.stdout.reconfigure(encoding="utf-8")

def remove_diacritics(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text) if unicodedata.category(c) != "Mn")

"""Tests
print(remove_diacritics("aée & c")) 
print(remove_diacritics("Český ráj")) 
print(remove_diacritics("München"))  
print(remove_diacritics("東京"))  
"""

def remove_all_diacritics(ref_object):
    if not ref_object or ref_object == "N/A":
        return
    affil = ref_object.get("affiliation", [])
    if not affil:
        return
    if not isinstance(affil, list):
        affil = [affil]
    for aff in affil:
        if aff == "N/A":
            continue
        city = aff.get("affiliation-city", "N/A")
        country = aff.get("affiliation-country", "N/A")
        institution = aff.get("affilname", "N/A") 
        if not city:
            city = "N/A"
        if not country:
            country = "N/A"
        if not institution:
            institution = "N/A"  
        aff["affiliation-country"] = remove_diacritics(country)
        aff["affiliation-city"] = remove_diacritics(city)
        aff["affilname"] = remove_diacritics(institution)


for filename in os.listdir("data_by_year"):
    if filename.endswith(".json"):
        with open(os.path.join("data_by_year", filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        for article in data:
            if "citedby_articles" in article and article["citedby_articles"] != "N/A":
                if isinstance(article["citedby_articles"], list):
                    for cited_article in article["citedby_articles"]:
                        remove_all_diacritics(cited_article)
                else:
                    remove_all_diacritics(article["citedby_articles"])

            if "references" in article and article["references"] != "N/A":
                if isinstance(article["references"], list):
                    for ref in article["references"]:
                        remove_all_diacritics(ref) 
                else:
                    remove_all_diacritics(article["references"])
        with open(os.path.join("data_by_year", filename), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)