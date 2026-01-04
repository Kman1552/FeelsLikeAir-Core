import os
from dotenv import load_dotenv
from openaq import OpenAQ

# 1. Load the variables from the .env file into the system environment
load_dotenv()

# 2. Grab the specific key using os.getenv
api_key = os.getenv("OPENAQ_API_KEY")

# 3. Use it in your client
if api_key:
    with OpenAQ(api_key=api_key) as client:
        # Your Week 1 logic starts here
        print("Successfully connected with API Key!")
else:
    print("Error: Could not find OPENAQ_API_KEY in .env file.")