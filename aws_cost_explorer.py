import os
from dotenv import load_dotenv
import boto3
import pandas as pd
from sqlalchemy import create_engine

def configure_aws_client(region_name, aws_access_key_id, aws_secret_access_key):
    return boto3.client('ce', region_name=region_name,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

def get_cost_and_usage_data(client, start_date, end_date, granularity, metrics, dimensions):
    try:
        # Create the request to get the data
        request = {
            'TimePeriod': {
                'Start': start_date,
                'End': end_date
            },
            'Granularity': granularity,
            'Metrics': metrics,
            'GroupBy': [{'Type': 'DIMENSION', 'Key': dim} for dim in dimensions]
        }

        # Make the API call to retrieve data
        response = client.get_cost_and_usage(**request)

        # Convert the data to a DataFrame
        data = []
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                data_point = {
                    'Date/Time Stamp': result['TimePeriod']['Start'],
                    'Service': group['Keys'][0],
                    'Resource Type': group['Keys'][1],
                    'Region': group['Keys'][2],
                    'Usage Type': group['Keys'][3],
                    'Account': group['Keys'][4],
                    'Cost': group['Metrics']['BlendedCost']['Amount'],
                    'Usage Metrics': group['Metrics']['UsageQuantity']['Amount'],
                    'Tags': str(group.get('Tags', [])),
                    'Savings Plans and Reserved Instances': str(group.get('SavingsPlansPurchaseRecommendationDetails', [])),
                    'Currency': response['ResponseMetadata']['HTTPHeaders']['content-currency'],
                }
                data.append(data_point)

        df = pd.DataFrame(data)
        return df

def insert_data_to_postgres(df, postgres_url, table_name):
    try:
        engine = create_engine(postgres_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data inserted into PostgreSQL table '{table_name}' successfully.")

    except Exception as e:
        print(f"An error occurred while inserting data into PostgreSQL: {str(e)}")

def main(config):
    # Create AWS client with configured access keys
    client = configure_aws_client(config['region_name'],
                                  config['aws_access_key_id'],
                                  config['aws_secret_access_key'])

    # Retrieve cost and usage data
    df = get_cost_and_usage_data(client, **config)

    # Check if data retrieval was successful
    if df is not None:
        # Insert data into PostgreSQL database
        insert_data_to_postgres(df, config['postgres_url'], config['table_name'])

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Configuration
    configuration = {
        'region_name': 'us-east-1',  # Replace with your desired AWS region
        'aws_access_key_id': os.getenv("AWS_ACCESS_KEY_ID"),
        'aws_secret_access_key': os.getenv("AWS_SECRET_ACCESS_KEY"),
        'start_date': '2023-01-01',
        'end_date': '2023-01-31',
        'granularity': 'DAILY',
        'metrics': ['BlendedCost', 'UsageQuantity'],
        'dimensions': ['SERVICE', 'RESOURCE_TYPE', 'REGION', 'USAGE_TYPE', 'LINKED_ACCOUNT'],
        'postgres_url': os.getenv("POSTGRES_URL"),
        'table_name': 'cost_usage_data'  # Replace with your desired table name
    }

    main(configuration)
