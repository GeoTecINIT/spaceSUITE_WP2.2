import pandas as pd
from sklearn.model_selection import train_test_split

path = 'Data/'
files = ['Euraxess_GNSS.xlsx', 'Euraxess_Satcom.xlsx', 'Indeed_GNSS.xlsx', 'Indeed_Satcom.xlsx', 
         'LinkedIn_GNSS.xlsx', 'LinkedIn_Satcom.xlsx', 'SpaceIndividuals_GNSS.xlsx', 'SpaceIndividuals_Satcom.xlsx']

new_df = pd.DataFrame()

for excel_file in files:
    df = pd.read_excel(path + excel_file)
    
    # Splitting data: Train (99%) and Test (1%)
    _, sampled_df = train_test_split(df, test_size=0.005, random_state=42)
    
    # Columns to concatenate
    columns = ['Title', 'OfferDescription', 'Requirements', 'Responsibilities', 'AdditionalInformation', 'Job_title', 'Job_Title', 'Job_description', 'Job_function', 'Industry']
    existing_columns = [col for col in columns if col in df.columns]

    # Concatenate the selected columns into a single string
    sampled_df['Concatenated'] = sampled_df[existing_columns].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
    
    # Create a new DataFrame with 'Concatenated' column renamed to 'Descriptions'
    temp_df = pd.DataFrame({'Descriptions': sampled_df['Concatenated']})
    
    # Handle 'Requirements' column if it exists
    if 'Requirements' in df.columns:
        requirements = sampled_df['Requirements'].tolist()
    else:
        requirements = ['-' for _ in range(len(sampled_df))]
    
    # Convert requirements list to DataFrame
    requirements_df = pd.DataFrame({'Requirements': requirements})
    
    # Concatenate 'Descriptions' and 'Requirements' columns
    combined_df = pd.concat([temp_df, requirements_df], axis=1)

    # Append to the new_df
    new_df = pd.concat([new_df, combined_df], ignore_index=True)

# Save the combined DataFrame to an Excel file
new_df.to_excel('test_mixed_data.xlsx', index=False)