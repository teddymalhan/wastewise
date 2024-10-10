# langchain_helper.py
import os
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from neo4j import GraphDatabase
import openai
from openai import OpenAI
from faiss_helper import load_faiss_index, search_similar_items
import numpy as np
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the OPENAI_API_KEY environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

index = load_faiss_index('faiss.index')
item_names = np.load('item_names.npy').tolist()

# Neo4j connection settings
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "testpassword"))

def generate_embedding_for_query(object_name):
    # Call the OpenAI API to create an embedding
    response = openai.embeddings.create(
        input=object_name,  # The text to embed (item name)
        model="text-embedding-ada-002"  # Model to use for embedding
    )
    return response.data[0].embedding

# Function to retrieve bin classification using Neo4j
def retrieve_bin_for_object(object_name):
    """
    Retrieves the bin type for an object from Neo4j if it exists.
    """
    with driver.session() as session:
        query = """
        MATCH (g:Item {name: $object_name})-[:SHOULD_GO_IN]->(b:Bin)
        RETURN b.type AS bin_type
        """
        result = session.run(query, object_name=object_name)
        # record.single() returns a single record or None if no records are found
        # eg: record = {"bin_type": "recyclable"}
        record = result.single()
        if record:
            return record["bin_type"]
        return "None"

# Function to generate a plausible bin classification using context from Neo4j and LangChain
def generate_guess(object_name):
    """
    If no exact match is found, use LangChain and an LLM to generate a plausible guess.
    """
    # Retrieve similar objects from Neo4j to use as context
    # with driver.session() as session:
    #     query = """
    #     MATCH (g:Item)-[:SHOULD_GO_IN]->(b:Bin)
    #     RETURN g.name AS similar_item, b.type AS bin_type LIMIT 5
    #     """
    #     results = session.run(query)
    #     context = "\n".join([f"{record['similar_item']} goes into {record['bin_type']}" for record in results])

    # # Use the retrieved data as context to generate a guess
    # prompt = f"Based on the following context:\n{context}\nWhere should '{object_name}' go?"
    # print(prompt)

    # # Call the LLM to generate a guess
    # response = client.chat.completions.create(model="gpt-4o-mini",
    # messages=[
    #         {"role": "system", "content": "You are an AI assistant that helps classify waste items into appropriate bins."},
    #         {"role": "user", "content": prompt}
    #     ],
    # max_tokens=50)

    # return response

    query_embedding = generate_embedding_for_query(object_name)

    # Find similar items using Faiss (the Facebook Algorithm)
    similar_items = search_similar_items(query_embedding, index, item_names, top_k=5)

    # Prepare context from similar items
    context_lines = []
    for item in similar_items:
        bin_type = retrieve_bin_for_object(item)
        context_lines.append(f"{item} goes into {bin_type}")
    context = "\n".join(context_lines)

    # Generate a prompt using the context 
    prompt = f"Based on the following context:\n{context}\nWhere should '{object_name}' go?"

     # Call the LLM to generate a guess
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI assistant that classifies waste items into bins. Your task is to respond only with the bin type, such as 'garbage bin', 'yellow bin', 'blue bin', or 'green bin'. Provide no explanation, no extra text, and no formatting."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )

    return (response.choices[0].message.content)