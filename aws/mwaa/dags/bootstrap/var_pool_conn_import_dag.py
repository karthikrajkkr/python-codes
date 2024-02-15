import os
import json
import boto3
import base64
import requests
import tempfile
from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator


def mwaa_host_token():
    mwaa = boto3.client("mwaa", region_name="us-east-1")
    mwaa_cli_token = mwaa.create_cli_token(Name="<airflow_environment_name>") #mwaa airflow environment name
    mwaa_auth_token = "Bearer " + mwaa_cli_token["CliToken"]
    mwaa_webserver_hostname = "https://{0}/aws_mwaa/cli".format(
        mwaa_cli_token["WebServerHostname"]
    )
    return mwaa_auth_token, mwaa_webserver_hostname


def mwaa_api_response(mwaa_webserver_hostname, mwaa_auth_token, raw_data):
    mwaa_response = requests.post(
        mwaa_webserver_hostname,
        headers={
            "Authorization": mwaa_auth_token,
            "Content-Type": "text/plain",
        },
        data=raw_data,
    )
    print(mwaa_response.status_code)
    mwaa_std_err_message = base64.b64decode(mwaa_response.json()["stderr"]).decode(
        "utf8"
    )
    mwaa_std_out_message = base64.b64decode(mwaa_response.json()["stdout"]).decode(
        "utf8"
    )
    print(mwaa_std_err_message)
    print(mwaa_std_out_message)


def af_object_s3(td, af_obj, team_name):
    s3 = boto3.resource("s3", region_name="us-east-1")
    af_bucket = s3.Bucket("<s3_bucket_name>")                             #bucket where conf files kept

    env = Variable.get("env")
    dev_tmp, def_tmp = {}, {}

    for obj in af_bucket.objects.filter(Prefix="config/"):
        if f"{team_name}/{af_obj}/{env}.json" in obj.key:
            dev_tmp = f"{td}/{os.path.basename(obj.key)}"
            af_bucket.download_file(obj.key, dev_tmp)
        elif f"{team_name}/{af_obj}/default.json" in obj.key:
            def_tmp = f"{td}/{os.path.basename(obj.key)}"
            af_bucket.download_file(obj.key, def_tmp)
    return dev_tmp, def_tmp


def af_import(**kwargs):
    airflow_obj = kwargs["airflow_obj"]
    command = kwargs["command"]
    team = kwargs["dag_run"].conf["team"]

    mwaa_auth_token, mwaa_webserver_hostname = mwaa_host_token()
    td = tempfile.TemporaryDirectory()
    dev_path, def_path = af_object_s3(td.name, airflow_obj, team)

    for fle in [dev_path, def_path]:
        if not isinstance(fle, dict) and os.stat(fle).st_size != 0:
            print(f"Parsing file : {os.path.basename(fle)}".center(100, "*"))
            with open(f"{fle}", "r") as jsn_file:
                fileconf = jsn_file.read().replace("\n", "")
            json_dictionary = json.loads(fileconf)
            for key in json_dictionary:
                print(key, " ", json_dictionary[key])
                if airflow_obj == "connections":
                    del_conn = f"connections delete {key}"
                    mwaa_api_response(
                        mwaa_webserver_hostname, mwaa_auth_token, del_conn
                    )

                raw_data = command.format(
                    key, str(json_dictionary[key]).replace("'", '"'), f"pools for {key}"
                )
                mwaa_api_response(mwaa_webserver_hostname, mwaa_auth_token, raw_data)
            print("-" * 100)
        else:
            print(f"File is empty or not available!!!")
    td.cleanup()


with DAG(
    "my_bootstrap_dag", schedule_interval=None, start_date=datetime(2024, 2, 12)
) as dag:
    start = DummyOperator(task_id="start")

    variable_import = PythonOperator(
        task_id="variable_import",
        python_callable=af_import,
        op_kwargs={"airflow_obj": "variables", "command": "variables set {0} {1}"},
    )

    pool_import = PythonOperator(
        task_id="pool_import",
        python_callable=af_import,
        op_kwargs={"airflow_obj": "pools", "command": "pools set {0} {1} '{2}' "},
    )

    conn_import = PythonOperator(
        task_id="connection_import",
        python_callable=af_import,
        op_kwargs={
            "airflow_obj": "connections",
            "command": """connections add {0} --conn-json '{1}' """,
        },
    )
    end = DummyOperator(task_id="end")

    start >> variable_import >> pool_import >> conn_import >> end
