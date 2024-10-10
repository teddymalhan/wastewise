from langchain_helper import retrieve_bin_for_object, generate_guess
from typing import Dict

def classify_object(object_name: str) -> Dict[str, str]:
    """
    Classify an object into a bin type.
    Uses a combination of Neo4j and LangChain to classify the object.

    Returns:
        dict: {
            "object_name": str,
            "bin_type": str
        }
    """
    # Try to retrieve the bin type from Neo4j
    bin_type = retrieve_bin_for_object(object_name)
    if bin_type and bin_type != "None":
        return {"object_name": object_name, "bin_type": bin_type}

    guesstimate_bin = generate_guess(object_name)
    
    return {"object_name": object_name, "bin_type": guesstimate_bin}