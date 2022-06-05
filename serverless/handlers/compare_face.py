import boto3
from datetime import datetime
from os import environ
import base64

BUCKET = 'video-temp-faas-muii'
COLLECTION = 'rekognition_collection'

def handler(event, context):
	time = datetime.now().timestamp()

	rekognition = boto3.client("rekognition")
	dynamo = boto3.client('dynamodb')
	s3 = boto3.client('s3')

	based_data = event['body']
	decode = base64.decodebytes(based_data.encode('utf-8'))
	img_inbytes =  decode.decode('utf-8').split('\n')[3][:-1]

	with open("/tmp/{}{}".format(time,".png"), "wb") as g:
		g.write(base64.decodebytes(img_inbytes.encode()))

	# Upload to S3
	s3.upload_file("/tmp/{}{}".format(time,".png"), BUCKET, "{}{}".format(time,'.png'))

	response = rekognition.search_faces_by_image(
		Image={
			"S3Object": {
				"Bucket": BUCKET,
				"Name": "{}{}".format(time,".png"),
			}
		},
		CollectionId=COLLECTION,
		FaceMatchThreshold=80,
		
	)

	find_person = response['FaceMatches'][0]['Face']['ExternalImageId'] #FaceId
	
	dynamo.put_item(
		TableName='processed_data_table',
		Item={
			'PersonId': {'S' : find_person},
			'Time': {'N': str(time)}
		}
	)

	
