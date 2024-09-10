from langchain_core.language_models.llms import LLM
import json
from pathlib import Path


def get_model_title(llm: LLM):
    """returns model title in a form <LangChain class>-<model title>"""
    llm_class = llm.__class__.__name__
    model_string = llm.model_name if hasattr(llm, "model_name") else str(llm.model)
    model_string = model_string.replace("/", "-")
    return f"{llm_class}_{model_string}"


def jsonl_to_json(input_file: str):
    """
    Converts a JSONL file to a JSON file with the same name but a .json extension.

    Args:
        input_file (str): Path to the input JSONL file.
    """
    # Automatically generate the output file name by replacing the .jsonl extension with .json
    output_file = str(input_file)[:-1]

    # Initialize an empty list to hold all the JSON objects
    json_array = []

    # Read the JSONL file and append each object to the list
    with open(input_file, 'r') as f:
        for line in f:
            # Parse each line (which is a JSON object)
            json_obj = json.loads(line)
            json_array.append(json_obj)

    # Write the list of JSON objects to a single JSON file
    with open(output_file, 'w') as f:
        json.dump(json_array, f, indent=4)

    print(f"Successfully converted {input_file} to {output_file}")
