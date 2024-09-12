import pandas as pd


def sheet_to_df(url):
    # Extract the sheet ID from the URL
    sheet_id = url.split('/')[5]
    
    # Construct the CSV export URL
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    
    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(csv_url)
    
    return df


def sheet_dataset_prepare(df_name="aws/en"):
    df2url = {
        "aws/en": "https://docs.google.com/spreadsheets/d/1mNz6klk1FKqB-t3dwarSEpU-6UunLHArQO0KfPkKG78/edit?gid=1956418441#gid=1956418441",
        "aws/ru": "https://docs.google.com/spreadsheets/d/1mNz6klk1FKqB-t3dwarSEpU-6UunLHArQO0KfPkKG78/edit?gid=1259270336#gid=1259270336",
    }
    variuos_columns = ['id', 'text', 'lang', 'type_general', 'judge_input', 'vul_deepeval']

    df = sheet_to_df(df2url[df_name])
    df = df.dropna(subset=variuos_columns)

    return df

# Usage
#url = "https://docs.google.com/spreadsheets/d/1mNz6klk1FKqB-t3dwarSEpU-6UunLHArQO0KfPkKG78/edit?gid=1956418441#gid=1956418441"
#df = sheet_to_df(url)
