import openai
from neo4j import GraphDatabase
from dotenv import load_dotenv
import csv
import os

# Load the .env file
load_dotenv()

# Get the OPENAI_API_KEY environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Neo4j connection setup
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "testpassword"))

# Function to generate embedding using OpenAI
def generate_embedding(item_name):
    # Call the OpenAI API to create an embedding
    response = openai.embeddings.create(
        input=item_name,  # The text to embed (item name)
        model="text-embedding-ada-002"  # Model to use for embedding
    )
    return response.data[0].embedding

# Function to store the item and embedding in Neo4j
def store_in_neo4j(item_name, bin_type, embedding):
    with driver.session() as session:
        # Run the Cypher query to create nodes and relationships
        session.run("""
        CREATE (i:Item {name: $item_name, embedding: $embedding})
        CREATE (b:Bin {type: $bin_type})
        CREATE (i)-[:SHOULD_GO_IN]->(b)
        """, item_name=item_name, bin_type=bin_type, embedding=embedding)

# Main function to load data from CSV and process
def process_csv_and_store(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item_name = row['item_name']  # Name of the item
            bin_type = row['bin_type']  # Bin type (recyclable, compost, etc.)
            
            # Generate embedding for the item name
            embedding = generate_embedding(item_name)
            if embedding:
                # Store the item, bin, and embedding in Neo4j
                store_in_neo4j(item_name, bin_type, embedding)
                print(f"Stored item '{item_name}' with embedding in Neo4j.")
            else:
                print(f"Failed to generate embedding for '{item_name}'.")

# Example usage:
csv_file_path = "./neo4j/final_cleaned_dataset.csv"  # Path to your CSV file
process_csv_and_store(csv_file_path)