
import boto3

BUCKET = "video_bucket.faas.muii"
KEY = "test.jpg" #Here must come from the trigger 
IMAGE_ID = KEY  # S3 key as ImageId
COLLECTION = "my-collection-id"


def handler(bucket, key, collection_id, image_id=None, attributes=(), region="eu-west-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.index_faces(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		CollectionId=collection_id,
		ExternalImageId=image_id,
	    DetectionAttributes=attributes,
	)
	return response['FaceRecords']