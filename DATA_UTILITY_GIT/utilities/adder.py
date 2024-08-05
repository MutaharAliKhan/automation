import pandas as pd
import os


def update_csv_with_filtered_values(final_df, second_csv_path):
    second_df = pd.read_csv(second_csv_path)
    header = second_df.columns
    if len(second_df) > 0:
        first_row = second_df.iloc[[0]]
        data_rows = second_df.iloc[1:]
    else:
        first_row = pd.DataFrame(columns=header)
        data_rows = pd.DataFrame(columns=header)

    common_columns = [col for col in header if col in final_df.columns]
    filtered_df = final_df[common_columns]
    filtered_df = filtered_df.drop_duplicates()
    updated_df = pd.concat([first_row, filtered_df], ignore_index=True)
    updated_df = updated_df.drop_duplicates()
    updated_df.to_csv(second_csv_path, index=False)
    return 1


def update_all_csvs_in_folder(final_csv_path, folder_path):
    final_df = pd.read_csv(final_csv_path)
    if final_df.empty:
        print(f"No data available in '{final_csv_path}'.")
        return 0

    updated_count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            second_csv_path = os.path.join(folder_path, filename)
            updated_count += update_csv_with_filtered_values(final_df, second_csv_path)

    if updated_count > 0:
        print(f"Total number of CSV files updated: {updated_count}")
    else:
        print(f"No CSV files were updated.")

    return updated_count


final_csv_path = 'D:\\MyRecentProjects\\Data_Utility\\final_dump\\joined_data.csv'
folder_path = 'D:\\MyRecentProjects\\Data_Utility\\updated_scripts'
update_all_csvs_in_folder(final_csv_path, folder_path)
