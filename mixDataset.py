import pandas as pd
from sklearn.model_selection import train_test_split

path = 'Data/'
files = ['Euraxess_GNSS.xlsx', 'Euraxess_Satcom.xlsx', 'Indeed_GNSS.xlsx', 'Indeed_Satcom.xlsx', 
         'LinkedIn_GNSS.xlsx', 'LinkedIn_Satcom.xlsx', 'SpaceIndividuals_GNSS.xlsx', 'SpaceIndividuals_Satcom.xlsx']

# Columns to check for a '1' and remove those rows
problematic_keywords = ['Robustness', 'Verification', 'Testing', 'Computer scientists', 'Physics', 'Secure Communications', 'Numerical simulations', 'Positioning', 'Cyber security', 'Cryptography', 'Receiver', 'Network management', 'Statistical analysis'] 

new_df = pd.DataFrame(columns=['Descriptions', 'Requirements'])

for excel_file in files:
    df = pd.read_excel(path + excel_file)
    
    # Filter to keep only the columns that exist in the DataFrame
    valid_columns_to_check = [col for col in problematic_keywords if col in df.columns]
    
    # If there are valid columns to check, remove rows with '1' in those columns
    if valid_columns_to_check:
        df_filtered = df[~df[valid_columns_to_check].eq(1).any(axis=1)]
    else:
        df_filtered = df  # If no valid columns, no filtering is applied
    
    # Splitting data: Train (95%) and Test (5%)
    _, sampled_df = train_test_split(df_filtered, test_size=0.05, random_state=42)
    
    # Columns to concatenate into the 'Descriptions' field
    columns = ['Title', 'OfferDescription', 'Requirements', 'Responsibilities', 'AdditionalInformation', 'Job_title', 'Job_Title', 'Job_description', 'Job_function', 'Industry']
    existing_columns = [col for col in columns if col in sampled_df.columns]

    # Create 'Descriptions' by concatenating the selected columns
    sampled_df['Descriptions'] = sampled_df[existing_columns].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
    
    # If 'Requirements' column exists, use it; otherwise, fill with '-'
    if 'Requirements' in sampled_df.columns:
        sampled_df['Requirements'] = sampled_df['Requirements'].fillna('-')
    else:
        sampled_df['Requirements'] = '-'
    
    if 'Keywords' not in sampled_df.columns:
        if 'Search_Keyword' in sampled_df.columns:
            sampled_df['Keywords'] = sampled_df['Search_Keyword']
        elif 'Keyword' in sampled_df.columns:
            sampled_df['Keywords'] = sampled_df['Keyword']
        else:
            sampled_df['Keywords'] = '-'
            
    # Select only 'Descriptions' and 'Requirements' columns for the final dataframe
    combined_df = sampled_df[['Descriptions', 'Requirements', 'Keywords']]

    # Append to the new_df
    new_df = pd.concat([new_df, combined_df], ignore_index=True)

# Save the combined DataFrame to an Excel file
new_df.to_excel('test_data.xlsx', index=False)