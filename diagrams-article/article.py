import os
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import DDB
from diagrams.aws.storage import S3
from diagrams.aws.network import ELB, APIGateway
from diagrams.aws.general import Users, User
from diagrams.aws.security import Cognito
from diagrams.custom import Custom
from diagrams.aws.ml import Rekognition
from diagrams.aws.integration import SQS

with Diagram("Añadir nuevo usuario", show=False, filename="./diagrams-article/añadir-nuevo-usuario"):
    # Users model
    users = User("Administrador")

    brad = Custom("Brad.Pitt.png", "./custom/train-bp-1-1.png")
    
    brad2 = Custom("Brad.Pitt.png", "./custom/train-bp-1-1.png")
    
    email = Custom("Send email to Brad.Pitt@alu.uclm.es", "./custom/email.png")

    vacio = Custom("", "")

    api_gw = APIGateway("API-Gateway")
        
    worker = Lambda('Upload face file')
            
    rekognition_train = Rekognition('Train model') 
        
    faces_img = S3('Person images')

    # SQS
    sub_topic = SQS('Subscription to topic "Brad.Pitt"')

    # Relations
    users >> brad >> api_gw >> worker
    
    worker >> brad2 >> rekognition_train
    brad2 >> faces_img >> rekognition_train
    worker >> rekognition_train
    worker >> sub_topic >> vacio >> email
    
    
with Diagram("Predecir usuario correctamente", show=False, filename="./diagrams-article/predecir-usuario"):
    # Users model
    users = User("Administrador")

    brad = Custom("Brad.Pitt.png", "./custom/train-bp-1-1.png")
    
    brad2 = Custom("Brad.Pitt.png", "./custom/train-bp-1-1.png")
    
    email = Custom("Send email to Brad.Pitt@alu.uclm.es", "./custom/email.png")

    vacio = Custom("", "")

    api_gw = APIGateway("API-Gateway")
        
    worker = Lambda('Upload face file')
            
    rekognition_train = Rekognition('Train model') 
        
    faces_img = S3('Person images')

    # SQS
    sub_topic = SQS('Subscription to topic "Brad.Pitt"')

    # Relations
    users >> brad >> api_gw >> worker
    
    worker >> brad2 >> rekognition_train
    brad2 >> faces_img >> rekognition_train
    worker >> rekognition_train
    worker >> sub_topic >> vacio >> email
    
    
with Diagram("Fallo al predecir usuario", show=False, filename="./diagrams-article/fallo-predecir-usuario"):
    # Users model
    users = User("Administrador")

    brad = Custom("Brad.Pitt.png", "./custom/train-bp-1-1.png")
    
    brad2 = Custom("Brad.Pitt.png", "./custom/train-bp-1-1.png")
    
    email = Custom("Send email to Brad.Pitt@alu.uclm.es", "./custom/email.png")

    vacio = Custom("", "")

    api_gw = APIGateway("API-Gateway")
        
    worker = Lambda('Upload face file')
            
    rekognition_train = Rekognition('Train model') 
        
    faces_img = S3('Person images')

    # SQS
    sub_topic = SQS('Subscription to topic "Brad.Pitt"')

    # Relations
    users >> brad >> api_gw >> worker
    
    worker >> brad2 >> rekognition_train
    brad2 >> faces_img >> rekognition_train
    worker >> rekognition_train
    worker >> sub_topic >> vacio >> email
