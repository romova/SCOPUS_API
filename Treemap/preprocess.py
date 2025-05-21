import sys
import os
import json
import base64
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

# Dictionaries for storing aggregated data
dict_city = {}
dict_country = {}
dict_institution = {}
dict_city_institution = {}

def get_affil_info(affil_obj, affil_type, year):
    """
    Extracts affiliation information from a given object and updates global dictionaries
    for country, city, institution, and city-institution statistics.
    """
    year = year - 1992
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

        # Normalize city name for Pilsen
        if city == "Plzen":
            city = "Pilsen"         

        # Use SHA1 hash of country name as unique identifier
        country_hash = base64.urlsafe_b64encode(hashlib.sha1(country.encode("utf-8")).digest()).decode("utf-8")
        
        # Update country-level statistics
        dict_country[country] = dict_country.get(country, [[0 for _ in range(2026-1992)], [0 for _ in range(2026-1992)], country_hash])
        dict_country[country][affil_type][year] += 1

        # Update city-level statistics (nested by country hash)
        if country_hash not in dict_city:
            dict_city[country_hash] = {}
        dict_city[country_hash][city] = dict_city[country_hash].get(city, [[0 for _ in range(2026-1992)], [0 for _ in range(2026-1992)]])
        dict_city[country_hash][city][affil_type][year] += 1

        # Update institution-level statistics (nested by country hash)
        if country_hash not in dict_institution:
            dict_institution[country_hash] = {}
        dict_institution[country_hash][institution] = dict_institution[country_hash].get(institution, [[0 for _ in range(2026-1992)], [0 for _ in range(2026-1992)]])
        dict_institution[country_hash][institution][affil_type][year] += 1

        # Update city-institution-level statistics (nested by country hash and city)
        if country_hash not in dict_city_institution:
            dict_city_institution[country_hash] = {}
        if city not in dict_city_institution[country_hash]:
            dict_city_institution[country_hash][city] = {}
        if institution not in dict_city_institution[country_hash][city]:
            dict_city_institution[country_hash][city][institution] = [[0 for _ in range(2026-1992)], [0 for _ in range(2026-1992)]]
        dict_city_institution[country_hash][city][institution][affil_type][year] += 1

# Iterate over all yearly data files and aggregate statistics
for filename in os.listdir("data_by_year"):
    if filename.endswith(".json"):
        with open(os.path.join("data_by_year", filename), "r", encoding="utf-8") as f:
            data = json.load(f)
            year = int(filename.split(".")[0].split("_")[-1])

        for article in data:
            # Process cited-by articles
            if "citedby_articles" in article and article["citedby_articles"] != "N/A":
                if isinstance(article["citedby_articles"], list):
                    for cited_article in article["citedby_articles"]:
                        get_affil_info(cited_article, 0, year)
                else:
                    get_affil_info(article["citedby_articles"], 0, year)

            # Process references
            if "references" in article and article["references"] != "N/A":
                if isinstance(article["references"], list):
                    for ref in article["references"]:
                        get_affil_info(ref, 1, year) 
                else:
                    get_affil_info(article["references"], 1, year)

# Output aggregated data to JSON files for later use
os.makedirs("processed/by_country", exist_ok=True)

countries_path = os.path.join("processed", "countries.json")
with open(countries_path, "w", encoding="utf-8") as f:
    json.dump(dict_country, f, ensure_ascii=False, indent=4)

for country, (cited_count, ref_count, country_hash) in dict_country.items():
    country_folder = os.path.join("processed/by_country", country_hash)
    os.makedirs(country_folder, exist_ok=True)

    city_path = os.path.join(country_folder, "cities.json")
    city_data = dict_city.get(country_hash, {})
    with open(city_path, "w", encoding="utf-8") as f:
        json.dump(city_data, f, ensure_ascii=False, indent=4)

    institution_path = os.path.join(country_folder, "institutions.json")
    institution_data = dict_institution.get(country_hash, {})
    with open(institution_path, "w", encoding="utf-8") as f:
        json.dump(institution_data, f, ensure_ascii=False, indent=4)

    city_institution_path = os.path.join(country_folder, "city_institutions.json")
    city_institution_data = dict_city_institution.get(country_hash, {})
    with open(city_institution_path, "w", encoding="utf-8") as f:
        json.dump(city_institution_data, f, ensure_ascii=False, indent=4)