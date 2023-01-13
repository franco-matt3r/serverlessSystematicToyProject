import json
import boto3
import os

s3 = boto3.client('s3')
DESTINATION_BUCKET = os.environ.get('DESTINATION_BUCKET')

def practiceProcessNewFile(event, context):    

    # obtain S3 data from the event source
    s3_bucket_start = json.loads(json.loads(event['Records'][0]['body'])['Message'])['Records'][0]['s3']['bucket']['name']
    file_name_start = json.loads(json.loads(event['Records'][0]['body'])['Message'])['Records'][0]['s3']['object']['key']
    print(s3_bucket_start, file_name_start)
    file = s3.get_object(Bucket=s3_bucket_start, Key=file_name_start)["Body"].read()
    file_content = json.loads(file)      
    
    # process data
    sum = 0
    manualCummulative = {}
    for i in file_content.items():
        sum+=i[1]
        manualCummulative[i[0]] = sum
    assert len(file_content.items()) == len(manualCummulative.items()), "The cummulative array should be the same length as the input array"
    jsonFile = json.dumps(manualCummulative).encode('utf-8')
    
    # save S3 data in 2nd bucket
    s3.put_object(Body=jsonFile, Bucket=DESTINATION_BUCKET, Key=file_name_start)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
