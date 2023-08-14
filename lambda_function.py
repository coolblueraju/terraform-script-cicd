import os
import json
import boto3
import psycopg2

def lambda_handler(event, context):
    # Retrieve the script name from the event payload
    script_name = event.get('postgres_script.sql')

    # Retrieve the PostgreSQL password from AWS Systems Manager Parameter Store
    parameter_name = '/umb/hcs/receiptvault/service/receiptvault-api/rds_password'  # Specify your Parameter Store parameter name
    password = get_parameter(parameter_name)

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host='umb-hcs-receiptvault-rds-dbinstance-ps.cluster-cm7vfbeoueuh.us-east-2.rds.amazonaws.com',
        port='5432',
        database='receiptvaultdb',
        user='receiptvault',
        password=password
    )

    try:
        # Download the PostgreSQL script from S3
        s3_bucket = 'hcs-rv-postgres-script-340638674143'
        s3_key = 'postgres_script.sql'
        script_content = download_script_from_s3(s3_bucket, s3_key)

        # Execute the PostgreSQL script
        cur = conn.cursor()
        cur.execute(script_content)
        conn.commit()

        response = {
            'status': 'success',
            'message': 'PostgreSQL script executed successfully'
        }
    except (Exception, psycopg2.DatabaseError) as error:
        response = {
            'status': 'error',
            'message': str(error)
        }
    finally:
        # Close the database connection
        if conn is not None:
            conn.close()

    return response

def download_script_from_s3(bucket, key):
    # Download the script file from S3
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    script_content = response['Body'].read().decode('utf-8')
    return script_content

def get_parameter(parameter_name):
    # Retrieve the PostgreSQL password from AWS Systems Manager Parameter Store
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    password = response['Parameter']['Value']
    return password