import json
from src.models import locationModel, OpenAQResponse, sensorModel, coordinateModel



with open('data/raw/location_8118.json', 'r') as f:
    raw_data = json.load(f)
loc_data = raw_data['results'][0]


#location validation
try:
    location = locationModel(**loc_data)
    print("Location data is valid:", location)
except ValueError as e:
    print("validation error in location data:", e)


#sensor validation
try:
    sensor = sensorModel(**loc_data['sensors'][0])
    print("Sensor data is valid:", sensor)
except ValueError as e:
    print("validation error in sensor data:", e)

    
#coordinate validation
try :
    coords = coordinateModel(**loc_data['coordinates'])
    print("Coordinate data is valid:", coords)
except ValueError as e:
    print("validation error in coordinate data:", e)


#flatterner
def flatten_location_data(validated_loc):
    flat_rows = []
    
    # Extract the common data (stuff that stays the same for every sensor)
    common_info = {
        "location_id": validated_loc.id,
        "location_name": validated_loc.name,
        "latitude": validated_loc.coordinates.latitude,
        "longitude": validated_loc.coordinates.longitude,
        "last_updated_utc": validated_loc.last_updated.utc
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