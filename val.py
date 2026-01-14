import json
from src.models import locationModel, OpenAQResponse, sensorModel, coordinateModel
import csv
import requests
import os   
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAQ_API_KEY")

location_IDS = [8557, 8192, 70631, 218205, 8039]  # dehli, kolkata, mumbai, bangalore, pune
base_url = "https://api.openaq.org/v3/locations"

def fetch_validate_location(loc_id):
    url = f"{base_url}/{loc_id}"
    try:
        headers = {"X-API-Key": API_KEY,
            "User-Agent": "AeroSense-Data-Pipeline/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        payload = response.json()
        # Validate the response using OpenAQResponse model

        raw_data = payload.get('results', [])[0] if payload.get('results') else payload

        validate_data = locationModel(**raw_data)
        return validate_data
    except Exception as e:
        print(f"error with ID {loc_id}: {e}")
        return None


def flatten_location_data(validated_loc):
    flat_rows = []
    
    # Extract the common data (stuff that stays the same for every sensor)
    common_info = {
    "location_id": validated_loc.id,
    "location_name": validated_loc.name,
    "latitude": validated_loc.coordinates.latitude,
    "longitude": validated_loc.coordinates.longitude,
    "last_updated_utc": validated_loc.datetime_last.utc.strftime("%Y-%m-%d %H:%M:%S")
}
    
    # Loop through each sensor and create a row
    for sensor in validated_loc.sensors:
        row = common_info.copy() # Start with the common info
        row.update({
            "sensor_id": sensor.id,
            "parameter": sensor.parameter.name,
            "value": getattr(sensor, 'value', 0.0), # Use 0.0 if value is missing
            "units": sensor.parameter.units
        })
        flat_rows.append(row)
        
    return flat_rows


def write_to_csv(flat_data, filename = "data/processed/air_data.csv"):
    import os
    os.makedirs(os.path.dirname(filename),exist_ok = True)

    if not flat_data:
        print("no data to write")
        return
    header = flat_data[0].keys()

    with open(filename, mode = 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(flat_data)

    print("data written to", filename)

def main():
    all_flat_rows = []
    for loc_id in location_IDS:
        print("fetching ID:", {loc_id})
        validated_loc = fetch_validate_location(loc_id) # fetching and validating location data

        if validated_loc:
            rows = flatten_location_data(validated_loc) # flattening the data to csv format
            all_flat_rows.extend(rows)
        
    if all_flat_rows:
        write_to_csv(all_flat_rows)
        print(f"data written successfully. {len(all_flat_rows)} sensor records") # if succesfull 

if __name__ == "__main__":
        main()