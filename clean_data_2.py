import sys
import os
import json


sys.stdout.reconfigure(encoding='utf-8')
dict_institution = {}
fix_count = 0

fixes = [
    ["Czech Republic", None, "Technical University", "Czech Republic", "Pilsen", "University of West Bohemia"],
    [None, None, "Technical University of Plzeň", "Czech Republic", "Pilsen", "University of West Bohemia"],
    [None, "Plzeň", None, "Czech Republic", "Pilsen", None],
    [None, "Plzen", None, "Czech Republic", "Pilsen", None],
    [None, "Brno-Chrlice", None, "Czech Republic", "Brno", None],
    [None, None, "European Centre of Excellence NTIS", "Czech Republic", "Pilsen", "University of West Bohemia"],
    [None, None, "Qinghai Minzu University", "China", "Xining", None],
    [None, None, "COMSATS University Islamabad", "Pakistan", "Islamabad", None],
    [None, None, "Carnegie Institution of Washington", "United States", "Washington", None],
    [None, None, "National Chin-Yi University of Technology", "Taiwan", "Taichung", None],
    [None, None, "Gyeongsang National University", "South Korea", "Jinju", None],
    [None, None, "University of Presov in Presov", "Slovakia", "Presov", None],
    [None, None, "Slovak Academy of Sciences", "Slovakia", "Bratislava", None],
    [None, None, "The Extreme Light Infrastructure ERIC", "Czech Republic", "Dolni Brezany", None],
    ["Czech Republic", None, "Faculty of Applied Sciences", "Czech Republic", "Pilsen", "University of West Bohemia"],
    [None, None, "New Technologies Research Centre", "Czech Republic", "Pilsen", "University of West Bohemia"],
    [None, None, "Jiangsu Nata Opto-Electronic Material Co. Ltd.", "China", "Suzhou", None],
    [None, None, "Evatec AG", "Switzerland", "Trubbach", None],
    ["Czech Republic", None, "NTIS - New Technologies for the Information Society", "Czech Republic", "Pilsen", "University of West Bohemia"],
    [None, None, "Science Center for Physics and Technology", "Ukraine", "Kharkiv", None],
    [None, None, "Instituto de Investigaciones en Matemáticas Aplicadas y en Sistemas", "Mexico", "Mexico City", None],
    ["Czech Republic", "Plzeo", None, None, "Pilsen", None],
    ["Czech Republic", None, "UWB", None, None, "University of West Bohemia"],
    ["Czech Republic", None, "New Technologies for the Information Society", None, None, "University of West Bohemia"],
    [None, None, "Al-Azhar University", "Egypt", "Cairo", None],
    ["Switzerland", "Geneva", None, None, "Geneva", None],
    ["Italy", "Roma", None, None, "Rome", None],
    [None, "České Budějovice", None, "Czech Republic", "Ceske Budejovice", None],
    ["Czech Republic", None, "NTIS", None, None, "University of West Bohemia"],
    [None, None, "University of Bohemia", None, "Pilsen", "University of West Bohemia"],
    ["France", None, "Hôpital Manhes", None, "Paris", None],
    [None, "Pilsen", "University of West", None, None, "University of West Bohemia"],
    [None, None, "JSC Power Machines", "Russia", "Saint Petersburg", None],
    ["United States", None, "University of Saint Joseph", None, "West Hartford", None],
    [None, None, "Regional Innovation Centre of Electrotechnic", None, "Pilsen", "University of West Bohemia"],
    [None, None, "not available", None, None, "N/A"],
    [None, None, "Joint Laboratory of Solid State Chemistry of the Czech Academy of Sciences and the University of Chemical Technology", "Czech Republic", "Pardubice", "University of Pardubice"],
    [None, None, "Ganzhou Achteck Tool Technology Co. Ltd.", "China", "Ganzhou", None],
    [None, None, "Czech Society for Ornithology", "Czech Republic", "Prague", None],
    [None, "Praha", None, "Czech Republic", "Prague", None],
    [None, "Ekaterinburg", None, "Russia", "Yekaterinburg", None],
    ["Ukraine", "Kharkov", None, None, "Kharkiv", None],
    ["Italy", "Turin", None, None, "Torino", None],
    ["China", None, "Huangshan College", None, "Huangshan", None],
    ["Egypt", "Kalubia", None, None, "Qalyubia", None],
    ["Indonesia", "South Jakarta", None, None, "Jakarta", None],
    [None, "Washington, D.C.", None, "United States", "Washington", None],
    ["China", "Baise City", None, None, "Baise", None],
]          

def get_affil_info(affil_obj):
    global dict_institution
    global fixes
    global fix_count
    for fix in fixes:
        fix_count += fix_it_all(affil_obj, fix[0], fix[1], fix[2], fix[3], fix[4], fix[5])
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
        if institution not in dict_institution:
            dict_institution[institution] = {}     
        dict_institution[institution][country+"-"+city] = dict_institution[institution].get(country+"-"+city, 0) + 1


def fix_it_all(affil_obj, if_country_is, if_city_is, if_institution_is, then_country_is, then_city_is, then_institution_is):
    if not affil_obj or affil_obj == "N/A":
        return 0
    affil = affil_obj.get("affiliation", [])
    if not affil:
        return 0
    count = 0
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
        if (country == if_country_is or if_city_is is None) and (city == if_city_is or if_city_is is None) and (institution == if_institution_is or if_institution_is is None):
            if then_country_is is not None:
                aff["affiliation-country"] = then_country_is
            if then_city_is is not None:    
                aff["affiliation-city"] = then_city_is
            if then_institution_is is not None:    
                aff["affilname"] = then_institution_is
            count += 1
    return count   


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
        with open(os.path.join("data_by_year", filename), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# we will print now institutions with more than 1 city-country pair
for institution in dict_institution:
    if len(dict_institution[institution]) > 1:
        print(f"{institution}:")
        for city_country in dict_institution[institution]:
            print(f"\t{city_country}: {dict_institution[institution][city_country]}")
# now we had plenty results to deal with
# some of them are duplicates, so we will remove them, some of them are not (Technical University: Pilsen, Mariupol,...) 
 


print(f"Fixes done now: {fix_count} (or maybe just matches all these Nones)") #Fixes done now: 3484
