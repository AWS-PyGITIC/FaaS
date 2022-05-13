import boto3

BUCKET = "video_bucket.faas.muii"
KEY = "search.jpg"
COLLECTION = "my-collection-id"

def search_faces_by_image(bucket, key, collection_id, threshold=80, region="ww"):
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

for record in search_faces_by_image(BUCKET, KEY, COLLECTION):
	face = record['Face']
	print ("Matched Face ({}%)".format(record['Similarity']))
	print ("  FaceId : {}".format(face['FaceId']))
	print ("  ImageId : {}".format(face['ExternalImageId']))
