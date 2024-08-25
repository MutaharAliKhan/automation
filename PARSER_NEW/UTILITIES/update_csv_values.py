import os
import pandas as pd


def update_multiple_columns_in_csv(directory, updates):
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(subdir, file)

                df = pd.read_csv(file_path)

                columns_updated = []
                for column_name, new_value in updates.items():
                    if column_name in df.columns:
                        df[column_name] = new_value
                        columns_updated.append(column_name)

                if columns_updated:
                    df.to_csv(file_path, index=False)
                    print(f"Updated columns {columns_updated} in file: {file_path}")


directory_path = r'D:\MyRecentProjects\Data_Utility\csv'
updates = {
    'username': 'Ali',
    'username1': 'Khan',
}

update_multiple_columns_in_csv(directory_path, updates)


# def update_csv_files_in_directory(directory, column_name, new_value):
#     for subdir, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.csv'):
#                 file_path = os.path.join(subdir, file)
#
#                 df = pd.read_csv(file_path)
#
#                 if column_name in df.columns:
#                     df[column_name] = new_value
#
#                     df.to_csv(file_path, index=False)
#                     print(f"Updated '{column_name}' in file: {file_path}")
#
#
# # Example usage:
# directory_path = r'D:\MyRecentProjects\Data_Utility\csv'
# update_csv_files_in_directory(directory_path, column_name='firstname', new_value='adsdsadsdsdsasd')

