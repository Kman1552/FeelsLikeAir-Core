import os
from openaq import OpenAQ
from pydantic import BaseModel
from dotenv import load_dotenv
import json

folder_path = "data/raw"
file_name = "location_8118.json"
full_path = os.path.join(folder_path, file_name)

# #load_dotenv()
# apiKey = os.getenv("OPENAQ_API_KEY")
# try:
#     client = OpenAQ(api_key=apiKey)
#     response = client.locations.get(8118).dict()
#     client.close()
#     print("Connection Successful")
# except Exception as e:
#     print("Connection Failed:", e)


with open(full_path, 'w') as file:
    data = json.dump(response, file, indent=4)
print("Data saved to", full_path)

class CoordinateM(BaseModel):

    Lat: float
    Lon : float


