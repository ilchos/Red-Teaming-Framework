import json
import pandas as pd


class GarakOutputParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.attempts = self._load_attempts()

    def _load_attempts(self):
        # Load the JSONL file and filter for objects with "entry_type": "attempt"
        attempts = []
        with open(self.file_path, 'r') as f:
            for line in f:
                obj = json.loads(line.strip())  # Parse each line as JSON
                if obj.get('goal'):
                    attempts.append(obj)
        return attempts

    def to_dataframe(self):
        # Convert the list of attempts to a pandas DataFrame
        return pd.DataFrame(self.attempts)


# Example usage
if __name__ == "__main__":
    # Replace with the path to your Garak output JSONL file
    file_path = 'path_to_garak_output.jsonl'

    # Create an instance of the parser
    parser = GarakOutputParser(file_path)

    # Convert the filtered attempts to a DataFrame
    df = parser.to_dataframe()

    # Display the DataFrame
    print(df.head())  # Display the first few rows of the DataFrame
