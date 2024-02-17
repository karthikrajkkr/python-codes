# S3 event -> SQS -> Trigger Event
import os
import boto3
import json
import requests
import base64


def s3_airflow_config(bucket):
    s3_client = boto3.client("s3", region_name = "us-east-1")    
    response = s3_client.get_object(Bucket=bucket, Key='config/airflow_config.json')
    airflow_config = response['Body'].read().decode('utf-8')
    return airflow_config
    
    
def trigger_dag(team, airflow_obj, mwaa_env_name):
    conf = str(json.dumps({'team':team, 'airflow_obj':airflow_obj}))
    mwaa = boto3.client("mwaa", region_name = "us-east-1")    
    mwaa_cli_token = mwaa.create_cli_token(Name=mwaa_env_name)
    
    mwaa_auth_token = 'Bearer ' + mwaa_cli_token['CliToken']
    mwaa_webserver_hostname = 'https://{0}/aws_mwaa/cli'.format(mwaa_cli_token['WebServerHostname'])
    dag_name = os.environ["dag_name"]
    raw_data = "dags trigger {0} -c '{1}'".format(dag_name, conf)
    
    mwaa_response = requests.post(
          mwaa_webserver_hostname,
          headers={
              'Authorization': mwaa_auth_token,
              'Content-Type': 'text/plain'
              },
          data=raw_data
          )
    
    print(mwaa_response.status_code)
    
    mwaa_std_err_message = base64.b64decode(mwaa_response.json()['stderr']).decode('utf8')
    mwaa_std_out_message = base64.b64decode(mwaa_response.json()['stdout']).decode('utf8')
    print(mwaa_std_err_message)
    print(mwaa_std_out_message)
    
    
def lambda_handler(event, context):
    print(event)
    
    bucket = eval(event['Records'][0]['body'])['Records'][0]['s3']['bucket']['name']
    path = eval(event['Records'][0]['body'])['Records'][0]['s3']['object']['key']
    path_split = path.split("/")
    
    airflow_config = s3_airflow_config(bucket)
    airflow_env = eval(airflow_config)['airflow_env']
    
    if path == "config/airflow_config.json":
        team = "admin"
        airflow_obj = "airflow_config"
        trigger_dag(team, airflow_obj, airflow_env)
        print(f"Triggered DAG for : {airflow_obj}")
    elif len(path_split)==4 and path.startswith("config/") and path.endswith(".json"):
        team = path_split[1]
        airflow_obj = path_split[2]
        trigger_dag(team, airflow_obj, airflow_env)
        print(f"Triggered DAG for : {airflow_obj}")
    else:
        print("Lambda Trigger because of non-config file. No action taken.")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
