import pandas as pd

def sheet_to_df(url):
    # Extract the sheet ID from the URL
    sheet_id = url.split('/')[5]
    
    # Construct the CSV export URL
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    
    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(csv_url)
    
    return df

# Usage
#url = "https://docs.google.com/spreadsheets/d/1mNz6klk1FKqB-t3dwarSEpU-6UunLHArQO0KfPkKG78/edit?gid=1956418441#gid=1956418441"
#df = sheet_to_df(url)
