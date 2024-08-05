import pandas as pd
import pathlib
import os


def join_csv_files_from_folder(folder_path, join_columns, output_file):
    """
    Join all CSV files in a specified folder on specified columns and save the result to a new CSV file.

    :param folder_path: Path to the folder containing the CSV files.
    :param join_columns: List of column names on which to join the CSV files.
    :param output_file: Path to the output CSV file where the joined data will be saved.
    """
    folder_path = pathlib.Path(folder_path)
    output_file = pathlib.Path(output_file)

    if not folder_path.is_dir():
        raise ValueError(f"The folder path {folder_path} is not a valid directory.")

    file_paths = list(folder_path.glob('*.csv'))

    if not file_paths:
        raise ValueError(f"No CSV files found in the folder {folder_path}.")

    dtype_dict = {col: str for col in join_columns}

    try:
        df_joined = pd.read_csv(file_paths[0], dtype=dtype_dict)
    except Exception as e:
        raise RuntimeError(f"Error reading the first file {file_paths[0]}: {e}")

    available_columns = [col for col in join_columns if col in df_joined.columns]

    if not available_columns:
        raise ValueError("None of the specified join columns are present in the first file.")

    for file_path in file_paths[1:]:
        try:
            df_next = pd.read_csv(file_path, dtype=dtype_dict)
        except Exception as e:
            print(f"Warning: Error reading file {file_path}: {e}")
            continue

        merge_columns = [col for col in available_columns if col in df_next.columns]

        if merge_columns:
            try:
                df_joined = pd.merge(df_joined, df_next, on=merge_columns, how='inner')
                available_columns = merge_columns
            except Exception as e:
                print(f"Warning: Error merging with file {file_path}: {e}")
                continue
        else:
            print(f"Warning: None of the join columns are present in {file_path}. Skipping this file.")

    for col in df_joined.select_dtypes(include=['float64']).columns:
        df_joined[col] = df_joined[col].map(lambda x: f"{x:.2f}" if pd.notnull(x) else x)

    try:
        df_joined.to_csv(output_file, index=False, float_format='%.2f')
    except Exception as e:
        raise RuntimeError(f"Error saving the output file {output_file}: {e}")

    print(f"Joined data has been saved to {output_file}")


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


# Define your folder paths and columns here
folder_path = 'D:\\MyRecentProjects\\Data_Utility\\dump'
join_columns = ['customer_number', 'account_type', 'run_number', 'check_digit', 'branch_code']
output_csv_path = 'D:\\MyRecentProjects\\Data_Utility\\final_dump\\joined_data.csv'

# Join the CSV files
join_csv_files_from_folder(folder_path, join_columns, output_csv_path)

# Update other CSV files with the joined data
update_folder_path = 'D:\\MyRecentProjects\\Data_Utility\\updated_scripts'
update_all_csvs_in_folder(output_csv_path, update_folder_path)
