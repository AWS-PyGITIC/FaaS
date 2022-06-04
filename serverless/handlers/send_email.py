                                                                             str(datetime.fromtimestamp(float(event['Records'][0]['dynamodb']['Keys']['Time']['N']))))
    
   topics = client.list_topics()

   for topic in topics['Topics']:
      person = event['Records'][0]['dynamodb']['Keys']['PersonId']['S']
      person = ''.join(person.split('.')[:-1])

      if person in topic['TopicArn']:
         response = client.publish(
            TopicArn = topic['TopicArn'],
            Message = message,
            Subject='Fichaje - FaaS'
         )import boto3
from datetime import datetime

def handler(event, context):
   client = boto3.client('sns')

   person = event['Records'][0]['dynamodb']['Keys']['PersonId']['S']
   person = '.'.join(person.split('.')[:-1])

   message = "Usted el usuario {} ha aparecido en la cámara a la hora {}.\n".format(person, 
       