import os
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import DDB
from diagrams.aws.storage import S3
from diagrams.aws.network import ELB, APIGateway
from diagrams.aws.general import Users
from diagrams.aws.security import Cognito
from diagrams.aws.ml import Rekognition
from diagrams.aws.integration import SQS
with Diagram("Infraestructure Diagram", show=False):


    # Users model
    users = Users("Usuarios")

    # All the stuff that is on the aws Infraestructure
    with Cluster('AWS'):

        # User validator
        #iam = Cognito('User validator')
        # Api Gateway
        api_gw = APIGateway("API-Gateway")
        # All the endpoints are lambda functions
        with Cluster("Funciones"):
            workers = [Lambda("Upload video frame"),
                       Lambda('Upload face file'),
                       Lambda("See your checks"),
                       Lambda('See all checks')
                       ]
        # All the vs with the trained model
        rekognition_train = Rekognition('Train model') 
        
        rekognition_predict = Rekognition('Predict') 
                    # The S3 sotorage
        main_storage = S3('Video frame storage')
        #storaged_trigger = Lambda("Send video to get faces")
        # Dynamo DB
        dynamo = DDB('Processed data')

        faces_img = S3('Person images')

        getvideoMetadata = Lambda('Inform users')

        # SQS
        queue = SQS('Email message')
        
        sub_topic = SQS('Subscription to topic')



    # Relations
    users << queue 
    users >> api_gw >> workers
    

    workers[0] >> main_storage >> rekognition_predict
    workers[0] >> rekognition_predict
    rekognition_predict >> dynamo >>  getvideoMetadata >> queue
    dynamo << workers[3]
    workers[1] >> faces_img >> rekognition_train
    workers[1] >> rekognition_train
    workers[1] >> sub_topic
    workers[2:3] >> dynamo
