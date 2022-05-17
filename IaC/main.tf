terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~>4.9"
    }
  }
}

provider "aws" {
  profile = "default"
  shared_config_files = [var.aws_config]
  shared_credentials_files = [var.aws_credentials]
}


resource "aws_vpc" "prod_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "Production"
  }
}

resource "aws_subnet" "prod_subnet-1" {
  vpc_id = aws_vpc.prod_vpc.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "Cluster-Subnet"
  }
}


#Create a API Gateway
resource "aws_api_gateway_rest_api" "prod_api" {
  name = "prod_api"
  description = "prod_api"
}


#############
## STORAGE ##
#############

# Create a S3 bucket for video uploads
resource "aws_s3_bucket" "video-bucket-faas-muii" {
  bucket = "video-bucket-faas-muii"
}

# Create a database with a timestamp and a person ID (at this moment, a person ID and a photo ID)
resource "aws_dynamodb_table" "processed_data_table" {
  name           = "processed_data_table"
  hash_key       = "PersonId"
  range_key      = "PhotoId"
  billing_mode   = "PAY_PER_REQUEST"
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
  attribute {
      name = "PersonId"
      type = "S"

    }
  
  attribute {
      name = "PhotoId"
      type = "S"

    }
  
}


#########
## SNS ##
#########

# Create a SNS topic for notifications
resource "aws_sns_topic" "email_topic" {
  name = "email_topic"
}

resource "aws_sns_topic_subscription" "email_target"{
  topic_arn = aws_sns_topic.email_topic.arn
  protocol = "email"
  endpoint = var.email
}



#############
## LAMBDAS ##
#############


resource "awscc_rekognition_collection" "rekognition_collection" {
  collection_id = "rekognition_collection"
  
}

#Create a Lambda function for upload a video
resource "aws_lambda_function" "upload_face_lambda" {
  filename = "handlers/upload_face.zip"
  function_name = "upload_face_lambda"
  role = var.aws_role
  handler = "main.handler"
  runtime = "python3.6"
  publish = true
}

#Create a Lambda function for detect a video
resource "aws_lambda_function" "compare_face" {
  filename = "handlers/compare_face.zip"
  function_name = "compare_face_lambda"
  role = var.aws_role
  handler = "main.handler"
  runtime = "python3.6"
  publish = true

  environment {
    variables = {
      COLLECTION = awscc_rekognition_collection.rekognition_collection.collection_id
    }
  }
}

#Create a Lambda function for send emails
resource "aws_lambda_function" "send_email" {
  filename = "handlers/send_email.zip"
  function_name = "send_email_lambda"
  role = var.aws_role
  handler = "main.handler"
  runtime = "python3.6"
  publish = true

  environment {
    variables = {
      topic_arn = aws_sns_topic.email_topic.arn
    }
  }
}
/*
#Create a Lambda function for see your checks
resource "aws_lambda_function" "prod_lambda_see_checks" {
  filename = "handlers/lambda_function_see_checks.zip"
  function_name = "prod_lambda_see_checks"
  role = var.aws_role
  handler = "main.handler"
  runtime = "python3.6"
  publish = true
}

#Create a Lambda function for see all checks
resource "aws_lambda_function" "prod_lambda_see_all_checks" {
  filename = "handlers/lambda_function_see_all_checks.zip"
  function_name = "prod_lambda_see_all_checks"
  role = var.aws_role
  handler = "main.handler"
  runtime = "python3.6"
  publish = true
}

#Create a Lambda function for upload face file
resource "aws_lambda_function" "prod_lambda_upload_face" {
  filename = "handlers/lambda_function_upload_face.zip"
  function_name = "prod_lambda_upload_face"
  role = var.aws_role
  handler = "main.handler"
  runtime = "python3.6"
  publish = true
}
*/

##############
## TRIGGERS ##
##############

# Create a trigger for send email lambda function
resource "aws_lambda_event_source_mapping" "lambda_send_email_trigger" {
  event_source_arn  = aws_dynamodb_table.processed_data_table.stream_arn
  function_name     = aws_lambda_function.send_email.arn
  starting_position = "LATEST"
#  batch_size        = 1
}

