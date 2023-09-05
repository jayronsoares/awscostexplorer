## AWS Cost Explorer Data Retrieval and Storage App

## Overview

The AWS Cost Explorer Data Retrieval and Storage App is a Python script designed to fetch cost and usage data from AWS Cost Explorer and store it in a PostgreSQL database. This app enhances the security of sensitive information, such as AWS access keys and database credentials, by using environment variables stored in a `.env` file.

## Features

- Secure Handling of Credentials: Sensitive information, including AWS access keys and database connection details, is securely managed using environment variables.

- AWS Cost Explorer Integration: The app interacts with AWS Cost Explorer via the AWS SDK to retrieve cost and usage data.

- Data Storage in PostgreSQL: Cost and usage data is stored in a PostgreSQL database, making it easy to analyze and query the data.

- Customizable Configuration: Users can configure the app by adjusting parameters such as AWS region, date range, granularity, metrics, dimensions, and the target database.

## Prerequisites

- Python: Ensure that Python is installed on your system.

- Required Python Packages: Install the required Python packages using pip:
  ```
  pip install python-dotenv boto3 pandas sqlalchemy
  ```

- AWS Account: You must have an AWS account with appropriate IAM permissions to access AWS Cost Explorer data.

- PostgreSQL Database: Set up a PostgreSQL database with the necessary privileges and connection details.

## Usage

1. Create a `.env` file: Create a file named `.env` in the same directory as the script and populate it with the following environment variables:

   ```
   AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
   AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
   POSTGRES_URL=postgresql://username:password@localhost:5432/database_name
   ```

   Replace placeholders with your actual credentials and database connection details.

2. Run the Script: Execute the script by running the following command in your terminal:

   ```
   python script_name.py
   ```

   Replace `script_name.py` with the actual name of your Python script.

3. Data Retrieval and Storage: The script will fetch AWS cost and usage data and store it in the specified PostgreSQL database table.

4. Monitor Progress: The script will provide progress updates and notify you when the data has been successfully inserted into the database.

## Customize Configuration

You can customize the configuration by adjusting the parameters in the `configuration` dictionary within the script. Modify settings such as AWS region, date range, granularity, metrics, dimensions, PostgreSQL connection URL, and table name according to your requirements.

## Security

- Sensitive Information: Sensitive information is stored securely in the `.env` file and loaded as environment variables, enhancing security and separation of concerns.

- IAM Permissions: Ensure that the IAM user associated with the AWS access keys has the necessary permissions to access AWS Cost Explorer data.

- Database Security: Configure your PostgreSQL database to have strong security measures and restricted access.

## License

This app is provided under the [MIT License](LICENSE).

## Disclaimer

This app is intended for educational and informational purposes. Use it responsibly and ensure compliance with AWS terms and conditions, as well as any applicable laws and regulations.
