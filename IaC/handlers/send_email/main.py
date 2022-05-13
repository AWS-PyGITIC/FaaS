import json
import logging
import boto3
import os

ARN = os.environ.get('topic_arn')

def handler(event, context):

   client = boto3.client('sns')
   message = "Photo recognition.\n"
    
   response = client.publish(
      TopicArn = ARN,
      Message = message + str(event),
      Subject='FaaS'
   )