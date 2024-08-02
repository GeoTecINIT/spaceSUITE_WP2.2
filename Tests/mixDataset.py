import pandas as pd
from sklearn.model_selection import train_test_split

path = './'
files = ['Space_Individuals_GNSS_Keywords.xlsx', 'Space_Individuals_Satcom_Keywords.xlsx']

new_df = pd.DataFrame()

for excel_file in files:
    df = pd.read_excel(path + excel_file)
    _, sampled_df = train_test_split(df, test_size=0.1, random_state=42)
    sampled_df['Concatenated'] = sampled_df[['Title', 'OfferDescription', 'Requirements']].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
    temp_df = sampled_df[['Concatenated', 'Requirements']].rename(columns={'Concatenated': 'Descriptions'})
    new_df = pd.concat([new_df, temp_df], ignore_index=True)

new_df.to_excel('test_mixed_data.xlsx', index=False)