# Script to display the bucket policy of all the s3 buckets in the AWS account
import json
import boto3

session = boto3.session.Session(profile_name="<name>", region_name="us-east-1")
s3 = session.client("s3")

for b in s3.list_buckets()['Buckets']:
    try:
        response = s3.get_bucket_policy(Bucket=b['Name'])
        print(b['Name'])
        print(json.dumps(eval(response['Policy']), indent=4))
        print("-".center(100,"-"))
    except:
        pass

