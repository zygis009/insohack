import pandas as pd
import json

def get_prompt(company_name: str, csv_path: str) -> str:
    df = pd.read_csv(csv_path)
    # print(dataframe.keys())

    nan_columns = df.columns[df.isna().iloc[0]].tolist()

    with open('prompt.txt', 'r') as file:
        prompt = file.read()
        json_keys = json.dumps(nan_columns)
        json_keys = json_keys.replace("[Company X]", company_name)
        prompt = prompt.replace("<REQUIRED_FIELDS>", json_keys)
        return prompt

if __name__ == '__main__':
    print(get_prompt("google", "../processed.csv"))