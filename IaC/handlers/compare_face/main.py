import boto3

BUCKET = "video_bucket.faas.muii"
KEY = "search.jpg"
COLLECTION = "my-collection-id"

def handler(bucket, key, collection_id, threshold=80, region="ww"):
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
