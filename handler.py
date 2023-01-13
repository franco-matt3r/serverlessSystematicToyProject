import json
import boto3

s3 = boto3.client('s3')

def practiceProcessNewFile(event, context):    
    # obtain S3 data
    s3_bucket_start = event['Records'][0]['s3']['bucket']['name']
    file_name_start = event['Records'][0]['s3']['object']['key']
    print("!!!1!!!", s3_bucket_start, file_name_start)
    file = s3.get_object(Bucket=s3_bucket_start, Key=file_name_start)["Body"].read()
    file_content = json.loads(file)      
    
    # process s3 data
    print("!!!2!!!",file_content["14176600"])
    sum = 0
    manualCummulative = {}
    for i in file_content.items():
        sum+=i[1]
        manualCummulative[i[0]] = sum
    assert len(file_content.items()) == len(manualCummulative.items()), "The cummulative array should be the same length as the input array"
    jsonFile = json.dumps(manualCummulative).encode('utf-8')
    
    # save s3 data
    s3_bucket_end = "franco-test-bucket2"
    file_path = file_name_start
    s3.put_object(Body=jsonFile, Bucket=s3_bucket_end, Key=file_path)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
