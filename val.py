import os
from openaq import OpenAQ
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("OPENAQ_API_KEY")
try:
    client = OpenAQ(api_key=apiKey)
    client.locations.get(8118)

    limit = 1000
    client.close()
    print("Connection Successful")
except Exception as e:
    print("Connection Failed:", e)

class CoordinateM(BaseModel):

    Lat: float
    Lon : float