import openai
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Set API key
openai_api = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api)

def generate_embedding_for_query(object_name):
    # Call the OpenAI API to create an embedding
    response = client.embeddings.create(
        input=object_name,  # The text to embed (item name)
        model="text-embedding-ada-002"  # Model to use for embedding
    )
    return response.data[0].embedding

print(generate_embedding_for_query("coffee cup"))