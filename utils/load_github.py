import requests
import pandas as pd
import json
from io import StringIO

class GithubFileLoader:
    def __init__(self, file_url):
        self.file_url = file_url
        self.raw_url = self._convert_to_raw_url(file_url)

    def _convert_to_raw_url(self, file_url):
        # Convert the GitHub file URL to the raw content URL
        if "github.com" not in file_url:
            raise ValueError("Invalid GitHub URL")

        raw_url = file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        return raw_url

    def _get_file_content(self):
        # Get the file content from the raw GitHub URL
        response = requests.get(self.raw_url)
        if response.status_code == 200:
            return response.text  # Return raw text content
        else:
            raise Exception(f"Failed to load file: {response.status_code}")

    def load_as_text(self):
        # Load the file content as plain text
        return self._get_file_content()

    def load_as_json(self):
        # Load the file content and parse it as JSON
        file_content = self._get_file_content()
        try:
            return json.loads(file_content)
        except json.JSONDecodeError:
            raise Exception("File is not a valid JSON")

    def load_as_jsonl(self):
        # Load the file content and parse it as JSONL (JSON Lines)
        file_content = self._get_file_content()
        json_lines = []
        try:
            for line in file_content.splitlines():
                json_lines.append(json.loads(line))
            return json_lines
        except json.JSONDecodeError:
            raise Exception("File is not a valid JSONL")

    def load_as_csv(self):
        # Load the file content as CSV using pandas
        file_content = self._get_file_content()
        try:
            csv_data = StringIO(file_content)  # Convert text to StringIO object for pandas
            return pd.read_csv(csv_data)  # Parse CSV content
        except Exception as e:
            raise Exception(f"Failed to parse CSV: {e}")


# Example usage
if __name__ == "__main__":
    # Example file URLs (replace these with actual GitHub file URLs)
    json_file_url = 'https://github.com/username/repo_name/blob/main/data/sample.json'
    jsonl_file_url = 'https://github.com/username/repo_name/blob/main/data/sample.jsonl'
    csv_file_url = 'https://github.com/username/repo_name/blob/main/data/sample.csv'
    text_file_url = 'https://github.com/username/repo_name/blob/main/data/sample.txt'

    loader = GithubFileLoader(json_file_url)

    # Load the file as JSON
    try:
        json_data = loader.load_as_json()
        print("JSON data loaded:", json_data)
    except Exception as e:
        print("Error loading JSON:", e)

    # Load the file as JSONL
    try:
        loader = GithubFileLoader(jsonl_file_url)
        jsonl_data = loader.load_as_jsonl()
        print("JSONL data loaded:", jsonl_data)
    except Exception as e:
        print("Error loading JSONL:", e)

    # Load the file as plain text
    try:
        loader = GithubFileLoader(text_file_url)
        text_data = loader.load_as_text()
        print("Text data loaded:", text_data)
    except Exception as e:
        print("Error loading text:", e)

    # Load the file as CSV
    try:
        loader = GithubFileLoader(csv_file_url)
        csv_data = loader.load_as_csv()
        print("CSV data loaded:")
        print(csv_data.head())  # Display the first few rows of the CSV data
    except Exception as e:
        print("Error loading CSV:", e)
