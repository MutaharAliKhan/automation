import os
import pandas as pd
import logging
import inspect
import database.database_operations as db_ops


script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
log_dir = os.path.join(project_root, 'logs')
log_file = os.path.join(log_dir, 'extractor.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

data_providers = {
    name: func
    for name, func in inspect.getmembers(db_ops, predicate=inspect.isfunction)
    if name.endswith('_data')
}

logging.debug(f"Discovered data provider functions: {data_providers}")


def data_provider(script_name):
    provider_func_name = f"{script_name.replace('.py', '')}_data"
    if provider_func_name in data_providers:
        result = data_providers[provider_func_name]()
        if not isinstance(result, (pd.DataFrame, dict)):
            raise ValueError(f"The function {provider_func_name} should return a DataFrame or a dict.")
        # Convert dict to DataFrame if needed
        return pd.DataFrame(result) if isinstance(result, dict) else result
    else:
        raise ValueError(f"No data provider function defined for script: {script_name}")


def update_csv(csv_path, data_frame):
    try:
        if os.path.exists(csv_path):
            existing_df = pd.read_csv(csv_path)
            logging.info(f"Processing existing CSV file: {csv_path}")

            if not data_frame.empty:
                header = existing_df.columns.tolist()
                common_columns = [col for col in header if col in data_frame.columns]

                if not common_columns:
                    logging.info(f"No matching columns between existing CSV and new data for {csv_path}.")
                    return

                data_frame = data_frame[common_columns]
                data_frame = data_frame.drop_duplicates()
                first_row = existing_df.iloc[0:1]
                combined_df = pd.concat([first_row, data_frame], ignore_index=True, sort=False)
                updated_df = combined_df.drop_duplicates(ignore_index=True)
                updated_df.to_csv(csv_path, index=False)

                # Calculate number of rows added
                initial_row_count = len(existing_df)
                updated_row_count = len(updated_df)
                if updated_row_count > initial_row_count:
                    rows_added = updated_row_count - initial_row_count
                    logging.info(f"Added {rows_added} new rows to {csv_path}.")
                else:
                    logging.info(f"No new rows were added to {csv_path}.")

                logging.info(f"Updated CSV file successfully: {csv_path}")
            else:
                logging.info(f"No new data to append to CSV file: {csv_path}")
        else:
            data_frame.to_csv(csv_path, index=False)
            logging.info(f"Created new CSV file: {csv_path}")

    except Exception as e:
        logging.error(f"Error updating CSV file {csv_path}: {e}")


def process_scripts(folder_path):
    total_files_processed = 0
    total_rows_added = 0

    try:
        for file in os.listdir(folder_path):
            if file.endswith('.py'):
                script_name = file
                csv_name = file.replace('.py', '.csv')
                csv_path = os.path.join(folder_path, csv_name)

                if script_name.replace('.py', '_data') in data_providers:
                    logging.info(f"Processing script: {script_name}")
                    data = data_provider(script_name)
                    if isinstance(data, pd.DataFrame):
                        initial_row_count = len(data)
                        update_csv(csv_path, data)
                        if not data.empty:
                            total_files_processed += 1
                            total_rows_added += initial_row_count
                    else:
                        logging.error(f"Data returned from {script_name} is not a DataFrame.")
                else:
                    logging.info(f"No action defined for script: {script_name}")

        logging.info(f"Total files processed: {total_files_processed}")
        logging.info(f"Total rows added: {total_rows_added}")

    except Exception as e:
        logging.error(f"Error processing scripts in folder {folder_path}: {e}")


if __name__ == '__main__':
    folder_path = os.path.join(project_root, 'updated_scripts')
    logging.info(f"Starting the data utility script with folder path: {folder_path}")
    process_scripts(folder_path)
    logging.info("Script execution completed.")
    with open(log_file, 'a') as log:
        log.write('\n')
