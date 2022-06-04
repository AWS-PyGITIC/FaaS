import boto3
from os import environ
import base64

BUCKET = 'video-bucket-faas-muii'
COLLECTION = 'rekognition_collection'

def handler(event, context):
	rekognition = boto3.client("rekognition")
	s3 = boto3.client('s3')

	based_data = event['body']
	decode = base64.decodebytes(based_data.encode('utf-8'))
	img_inbytes =  decode.decode('utf-8').split('\n')[3][:-1]
	img_ext =  decode.decode('utf-8').split('\n')[7][:-1]
	name =  ''.join(img_ext.split('.')[:-1])
	name_dot =  '.'.join(img_ext.split('.')[:-1])

	with open("/tmp/{}".format(img_ext), "wb") as g:
		g.write(base64.decodebytes(img_inbytes.encode()))

		
	# Upload to S3
	s3.upload_file("/tmp/{}".format(img_ext), BUCKET, img_ext)

	#Add into rekognition collection
	res = rekognition.index_faces(
		Image={
			"S3Object": {
				"Bucket": BUCKET,
				"Name": img_ext,
			}
		},
		CollectionId=COLLECTION,
		ExternalImageId=img_ext,
	)
	
	sns = boto3.client('sns')
	topic = sns.create_topic(Name=name)

	sns.subscribe(
            TopicArn=topic['TopicArn'],
            Protocol='email',
            Endpoint=name_dot+'@alu.uclm.es'
	)
