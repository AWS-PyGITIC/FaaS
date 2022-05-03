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
    with Cluster('aws'):

        # User validator
        iam = Cognito('User validator')
        # Api Gateway
        api_gw = APIGateway("Api-Gateway")
        # All the endpoints are lambda functions
        with Cluster("funciones"):
            workers = [Lambda("Upload video"),
                       Lambda('Upload Face file'),
                       Lambda("see your checks"),
                       Lambda('See all checks')
                       ]
        # All the vs with the trained model
        rekognition = Rekognition('rekognition') 
                    # The S3 sotorage
        main_storage = S3('Video storage')
        storaged_trigger = Lambda("Send video to get faces")
        # Dynamo DB
        dynamo = DDB('processed data')

        faces = DDB('Person Images')
        faces_img = S3('Person Images')

        getvideoMetadata = Lambda('Inform users')

        # SQS
        queue = SQS('email message')



    # Relations
    users << queue 
    users >> api_gw >> workers
    api_gw >> iam >> api_gw

    workers[0] >> main_storage >> storaged_trigger >> rekognition
    rekognition >> dynamo >>  getvideoMetadata >> queue
    dynamo << workers[3]
    workers[1] >> faces
    workers[1] >> faces_img
    workers[2:3] >> dynamo
    workers[2:3] >> faces