import os
import csv

mock_data = [
    {
        "customer_number": "12345",
        "account_type": "Savings",
        "run_number": "001",
        "check_digit": "9",
        "branch_code": "001",
        "transaction_amount": "500.00"
    },
    {
        "customer_number": "67890",
        "account_type": "Checking",
        "run_number": "002",
        "check_digit": "3",
        "branch_code": "002",
        "transaction_amount": "300.00"
    },
    {
        "customer_number": "24680",
        "account_type": "Checking",
        "run_number": "004",
        "check_digit": "7",
        "branch_code": "004",
        "transaction_amount": "450.00"
    }
]

mock_data2 = [
    {
        "customer_number": "12345",
        "account_type": "Savings",
        "run_number": "001",
        "check_digit": "9",
        "branch_code": "001",
        "account_balance": "1500.00"
    },
    {
        "customer_number": "67890",
        "account_type": "Checking",
        "run_number": "002",
        "check_digit": "3",
        "branch_code": "002",
        "account_balance": "200.00"
    },
    {
        "customer_number": "13579",
        "account_type": "Savings",
        "run_number": "003",
        "check_digit": "1",
        "branch_code": "003",
        "account_balance": "1200.00"
    },
    {
        "customer_number": "24680",
        "account_type": "Checking",
        "run_number": "004",
        "check_digit": "7",
        "branch_code": "004",
        "account_balance": "450.00"
    }
]

mock_data3 = [
    {
        "customer_number": "12345",
        "account_type": "Savings",
        "run_number": "001",
        "check_digit": "9",
        "branch_code": "001",
        "customer_name": "John Doe",
        "customer_email": "john.doe@example.com"
    },
    {
        "customer_number": "67890",
        "account_type": "Checking",
        "run_number": "002",
        "check_digit": "3",
        "branch_code": "002",
        "customer_name": "Jane Smith",
        "customer_email": "jane.smith@example.com"
    },
    {
        "customer_number": "13579",
        "account_type": "Savings",
        "run_number": "003",
        "check_digit": "1",
        "branch_code": "003",
        "customer_name": "Robert Brown",
        "customer_email": "robert.brown@example.com"
    },
    {
        "customer_number": "24680",
        "account_type": "Checking",
        "run_number": "004",
        "check_digit": "7",
        "branch_code": "004",
        "customer_name": "Lisa White",
        "customer_email": "lisa.white@example.com"
    }
]


def write_to_csv(data, table_name):
    # Ensure the dump directory exists
    dump_dir = os.path.join(os.path.dirname(__file__), '..\dump')
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    csv_file_path = os.path.join(dump_dir, f"{table_name}.csv")

    if data and isinstance(data, list) and len(data) > 0:
        keys = data[0].keys()
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f"Data written to CSV file: {csv_file_path}")
    else:
        print("No data to write to CSV.")


# Call the function to test
write_to_csv(mock_data, 'transaction')
write_to_csv(mock_data2, 'account')
write_to_csv(mock_data3, 'customer')
