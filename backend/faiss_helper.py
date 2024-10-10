import os
import faiss
import numpy as np
from neo4j import GraphDatabase

# Neo4j connection setup
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "testpassword"))

def get_all_embeddings():
    with driver.session() as session:
        result = session.run("""
            MATCH (i:Item)
            RETURN i.name AS name, i.embedding AS embedding
        """)
        item_names = []
        embeddings = []
        for record in result:
            item_names.append(record['name'])
            embeddings.append(record['embedding'])
        embeddings = np.array(embeddings, dtype='float32')
        return item_names, embeddings

def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def save_faiss_index(index, file_path='faiss.index'):
    faiss.write_index(index, file_path)

def load_faiss_index(file_path='faiss.index'):
    # Check if the index file exists
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist. Building the FAISS index.")
        item_names, embeddings = get_all_embeddings()
        index = build_faiss_index(embeddings)
        save_faiss_index(index, file_path)
        np.save('item_names.npy', np.array(item_names))
        return index
    else:
        print(f"Loading FAISS index from {file_path}.")
        index = faiss.read_index(file_path)
        return index

def update_faiss_index():
    item_names, embeddings = get_all_embeddings()
    index = build_faiss_index(embeddings)
    save_faiss_index(index)
    # Also save item names mapping
    np.save('item_names.npy', np.array(item_names))
    return index, item_names

def search_similar_items(query_embedding, index, item_names, top_k=10):
    query_embedding = np.array(query_embedding, dtype='float32').reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    similar_items = []
    for idx in indices[0]:
        similar_items.append(item_names[idx])
    return similar_items