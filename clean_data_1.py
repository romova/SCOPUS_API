import sys
import os
import json


sys.stdout.reconfigure(encoding='utf-8')
dict_city = {}
dict_country = {}
dict_institution = {}

def get_affil_info(affil_obj):
    global dict_city
    global dict_country
    global dict_institution
    if not affil_obj or affil_obj == "N/A":
        return
    affil = affil_obj.get("affiliation", [])
    if not affil:
        return
    if not isinstance(affil, list):
        affil = [affil]
    for aff in affil:
        if aff == "N/A":
            city = country = institution = "N/A"
        else:
            city = aff.get("affiliation-city", "N/A")
            country = aff.get("affiliation-country", "N/A")
            institution = aff.get("affilname", "N/A") 
        if not city:
            city = "N/A"
        if not country:
            country = "N/A"
        if not institution:
            institution = "N/A"      
        dict_city[country + "-" + city] = dict_city.get(country + "-" + city, 0) + 1
        dict_country[country] = dict_country.get(country, 0) + 1
        dict_institution[institution] = dict_institution.get(institution, 0) + 1

"""
def correct_countries(affil_obj, corrected_countries):
    if not affil_obj or affil_obj == "N/A":
        return
    affil = affil_obj.get("affiliation", [])
    if not affil:
        return
    if not isinstance(affil, list):
        affil = [affil]
    for aff in affil:
        if aff == "N/A":
            city = country = institution = "N/A"
        else:
            country = aff.get("affiliation-country", "N/A")
            if country in [c[0] for c in corrected_countries]:
                for c in corrected_countries:
                    if country == c[0]:
                        aff["affiliation-country"] = c[1]


for filename in os.listdir("data_by_year"):
    if filename.endswith(".json"):
        with open(os.path.join("data_by_year", filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        for article in data:
            if "citedby_articles" in article and article["citedby_articles"] != "N/A":
                if isinstance(article["citedby_articles"], list):
                    for cited_article in article["citedby_articles"]:
                        get_affil_info(cited_article)
                else:
                    get_affil_info(article["citedby_articles"])

            if "references" in article and article["references"] != "N/A":
                if isinstance(article["references"], list):
                    for ref in article["references"]:
                        get_affil_info(ref) 
                else:
                    get_affil_info(article["references"])


total = 0
for key, value in dict(sorted(dict_country.items(), key=lambda item: item[1])).items():
    print(f"{key}: {value}")    
    total += value
print(f"\n\nTotal: {total}, N/A: {dict_country['N/A']}")  


# [wrong in data, corrected]
corrected_countries = [
        ["Macedonia", "North Macedonia"], # 1 hit
        ["Libyan Arab Jamahiriya", "Libya"], # 1 hit
        ["Russia", "Russian Federation"] # 1 hit
    ]
#warning: we got 20*Czechoslovakia in records, but we don't know how to correct it yet

for filename in os.listdir("data_by_year"):
    if filename.endswith(".json"):
        with open(os.path.join("data_by_year", filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        for article in data:
            if "citedby_articles" in article and article["citedby_articles"] != "N/A":
                if isinstance(article["citedby_articles"], list):
                    for cited_article in article["citedby_articles"]:
                        correct_countries(cited_article, corrected_countries)
                else:
                    correct_countries(article["citedby_articles"], corrected_countries)

            if "references" in article and article["references"] != "N/A":
                if isinstance(article["references"], list):
                    for ref in article["references"]:
                        correct_countries(ref, corrected_countries) 
                else:
                    correct_countries(article["references"], corrected_countries)
        with open(os.path.join("data_by_year", filename), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

Total: 516038, N/A: 10226
"""

for filename in os.listdir("data_by_year"):
    if filename.endswith(".json"):
        with open(os.path.join("data_by_year", filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        for article in data:
            if "citedby_articles" in article and article["citedby_articles"] != "N/A":
                if isinstance(article["citedby_articles"], list):
                    for cited_article in article["citedby_articles"]:
                        get_affil_info(cited_article)
                else:
                    get_affil_info(article["citedby_articles"])

            if "references" in article and article["references"] != "N/A":
                if isinstance(article["references"], list):
                    for ref in article["references"]:
                        get_affil_info(ref) 
                else:
                    get_affil_info(article["references"])


total = 0
nas = 0
for key, value in dict(sorted(dict_city.items(), key=lambda item: item[0])).items():
    print(f"{key}: {value}")    
    total += value
    if key.endswith("N/A"):
        nas += value
print(f"\n\nTotal: {total}, N/A: {nas}")

"""
Now we got 
N/A-Amazon: 1 #this one has affil [N/A, Amazon, Alexa Speech]. We will not deal with it and let it as it is.
N/A-Berlin: 1
N/A-Brno: 1
N/A-Bucharest: 3
N/A-Cluj: 1
N/A-Cluj Napoca: 1
N/A-Dresden: 1
N/A-Iasi: 1
N/A-Kosice: 1
N/A-Kwai: 1
N/A-Macau: 1
N/A-N/A: 10198 # we cannot guess
N/A-Novi Sad: 1
N/A-Plzen: 7
N/A-Pristina, Kosovo: 1
N/A-Punchbowl: 1
N/A-Signal: 1 # we don't know what it is, but we will not deal with it also
N/A-St. Petersburg: 2
N/A-Surrey: 1 # could actually be in UK or Canada, so we will also not deal with it
N/A-Žilina: 1
where we can easily figure out countries in which these cities are located.
"""
# [city, coutry should be]
added_countries_to_cities = [
        ["Berlin", "Germany"],
        ["Brno", "Czech Republic"],
        ["Bucharest", "Romania"],
        ["Cluj", "Romania"],
        ["Cluj Napoca", "Romania"],
        ["Dresden", "Germany"],
        ["Iasi", "Romania"],
        ["Kosice", "Slovakia"],
        ["Kwai", "Thailand"],
        ["Macau", "China"],
        ["Novi Sad", "Serbia"],
        ["Plzen", "Czech Republic"],
        ["Pristina, Kosovo", "Kosovo"],
        ["Punchbowl", "Australia"],
        ["St. Petersburg", "Russia"],
        ["Žilina", "Slovakia"]
    ]

def correct_cities_countries(affil_obj, corrected_cities_countries):
    if not affil_obj or affil_obj == "N/A":
        return
    affil = affil_obj.get("affiliation", [])
    if not affil:
        return
    if not isinstance(affil, list):
        affil = [affil]
    for aff in affil:
        if aff != "N/A":
            city = aff.get("affiliation-city", "N/A")
            if city in [c[0] for c in corrected_cities_countries]:
                for c in corrected_cities_countries:
                    if city == c[0]:
                        if len(c) == 1:
                            print()
                        aff["affiliation-country"] = c[1]

for filename in os.listdir("data_by_year"):
    if filename.endswith(".json"):
        with open(os.path.join("data_by_year", filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        for article in data:
            if "citedby_articles" in article and article["citedby_articles"] != "N/A":
                if isinstance(article["citedby_articles"], list):
                    for cited_article in article["citedby_articles"]:
                        correct_cities_countries(cited_article, added_countries_to_cities)
                else:
                    correct_cities_countries(article["citedby_articles"], added_countries_to_cities)

            if "references" in article and article["references"] != "N/A":
                if isinstance(article["references"], list):
                    for ref in article["references"]:
                        correct_cities_countries(ref, added_countries_to_cities) 
                else:
                    correct_cities_countries(article["references"], added_countries_to_cities)
        with open(os.path.join("data_by_year", filename), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)                        