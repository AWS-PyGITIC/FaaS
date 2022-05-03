
import boto3

BUCKET = "amazon-rekognition"
KEY = "test.jpg"
IMAGE_ID = KEY  # S3 key as ImageId
COLLECTION = "my-collection-id"

# Note: you have to create the collection first!
# rekognition.create_collection(CollectionId=COLLECTION)

def index_faces(bucket, key, collection_id, image_id=None, attributes=(), region="eu-west-1"):
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


for record in index_faces(BUCKET, KEY, COLLECTION, IMAGE_ID):
	face = record['Face']
	# details = record['FaceDetail']
	print ("Face ({}%)".format(face['Confidence']))
	print ("  FaceId: {}".format(face['FaceId']))
	print ("  ImageId: {}".format(face['ImageId']))
