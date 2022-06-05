import boto3
import json
def handler(event, context):
    dynamo = boto3.client('dynamodb')

    items = dynamo.scan(TableName='processed_data_table')

    return {
        "statusCode": 200,
        "body": json.dumps({"checks": items['Items']}),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    