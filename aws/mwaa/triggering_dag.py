import boto3
import json
import requests
import base64

mwaa_env_name = '<env_name>'
dag_name = '<dag_name>'

## {{dag_run.conf}}
team = '<team_name>'
conf = str(json.dumps({'team':team}))

session = boto3.session.Session(profile_name = "mwaa")
mwaa = session.client("mwaa", region_name = "us-east-1")
mwaa_cli_token = mwaa.create_cli_token(Name=mwaa_env_name)
mwaa_auth_token = 'Bearer ' + mwaa_cli_token['CliToken']
mwaa_webserver_hostname = 'https://{0}/aws_mwaa/cli'.format(mwaa_cli_token['WebServerHostname'])
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
