import boto3
from os import environ
BUCKET = "video_bucket.faas.muii"
KEY = "search.jpg" ## here must be the face from the video-frame
if environ.get('COLLECTION') is not None:
	COLLECTION = environ.get('COLLECTION')
else:
	COLLECTION = 'rekognition_collection'

def handler(bucket, key, collection_id, threshold=80, region=""):
	rekognition = boto3.client("rekognition", region)

	response = rekognition.search_faces_by_image(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		CollectionId=collection_id,
		FaceMatchThreshold=threshold,
	)
	return response['FaceMatches']
