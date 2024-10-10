import csv
from neo4j import GraphDatabase

# Neo4j connection settings
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "testpassword"))

def load_csv_to_neo4j(csv_file_path):
    """
    Load data from CSV to Neo4j.
    """
    with driver.session() as session:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item = row['item']
                bin = row['bin']
                session.run("""
                    MERGE (i:Item {name: $item})
                    MERGE (b:Bin {type: $bin})
                    MERGE (i)-[:SHOULD_GO_IN]->(b)
                """, item=item, bin=bin)

# Example usage:
load_csv_to_neo4j("dataset.csv")