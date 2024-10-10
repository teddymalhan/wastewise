from langchain_helper import generate_guess

def test_classification(object_name: str) -> str:
    """
    Test driver for classifying an object using the generate_guess function.
    It will directly use the generate_guess function to generate a guess for the object's bin.
    """
    print(f"Testing classification for: '{object_name}'")

    # Call the generate_guess function
    guess_bin = generate_guess(object_name)

    # Output the result
    print(f"Classification Result: '{object_name}' should go into '{guess_bin}' bin.")
    return guess_bin

if __name__ == "__main__":
    # Example object names for testing
    test_objects = [
        "food soiled paper",
    ]

    # Run the test for each object
    for obj in test_objects:
        test_classification(obj)