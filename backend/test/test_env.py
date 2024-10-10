import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the OPENAI_API_KEY environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Print the key (or a message if it's not found)
if openai_api_key:
    print(f"OPENAI_API_KEY: {openai_api_key}")
else:
    print("OPENAI_API_KEY not found in environment variables.")