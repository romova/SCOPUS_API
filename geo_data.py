import pandas as pd
import time
from opencage.geocoder import OpenCageGeocode

# --- Load your existing data (replace with your actual file path) ---
df = pd.read_csv("agregace.csv")  # Replace with your CSV file if needed

# --- Setup OpenCage ---
key = "YOUR-API-KEY"  # Replace with your real API key
geocoder = OpenCageGeocode(key)

# --- Build cache to avoid repeated API calls ---
geo_cache = {}

# --- Function to get coordinates for (city, country) ---
def get_coordinates(city, country):
    if pd.isna(city) or pd.isna(country):
        return None, None
    
    query = f"{city}, {country}"
    if query in geo_cache:
        return geo_cache[query]
    
    try:
        results = geocoder.geocode(query)
        if results and len(results) > 0:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            geo_cache[query] = (lat, lng)
            time.sleep(1)  # To respect rate limits
            return lat, lng
    except Exception as e:
        print(f"Error with '{query}': {e}")
    
    geo_cache[query] = (None, None)
    return None, None

# --- Add latitude and longitude columns ---
df["latitude"] = None
df["longitude"] = None

for i, row in df.iterrows():
    city = row["city"]
    country = row["country"]
    lat, lng = get_coordinates(city, country)
    df.at[i, "latitude"] = lat
    df.at[i, "longitude"] = lng
    print(f"[{i+1}/{len(df)}] {row['name']} - {city}, {country} → ({lat}, {lng})")

# --- Save to new CSV file ---
df.to_csv("institutions_with_coordinates.csv", index=False)
print("Saved to institutions_with_coordinates.csv")