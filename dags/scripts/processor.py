import pandas as pd

def clean_data(input_path, output_path):
    data = pd.read_csv(input_path)
    cleaned_data = data.dropna()
    cleaned_data.to_csv(output_path)
    return output_path