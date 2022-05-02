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
## LAMBDAS ##
#############

#Create a Lambda function for upload a video
resource "aws_lambda_function" "prod_lambda" {
  filename = "lambda_function_upload.zip"
  function_name = "prod_lambda"
  role = var.aws_role
  handler = "upload_video.lambda_handler"
  runtime = "python3.6"
  publish = true
}

#Create a Lambda function for detect a video
resource "aws_lambda_function" "prod_lambda_detect" {
  filename = "lambda_function_detect.zip"
  function_name = "prod_lambda_detect"
  role = var.aws_role
  handler = "detect_video.lambda_handler"
  runtime = "python3.6"
  publish = true
}

#Create a Lambda function for send emails
resource "aws_lambda_function" "prod_lambda_send_email" {
  filename = "lambda_function_send_email.zip"
  function_name = "prod_lambda_send_email"
  role = var.aws_role
  handler = "send_email.lambda_handler"
  runtime = "python3.6"
  publish = true
}

#Create a Lambda function for see your checks
resource "aws_lambda_function" "prod_lambda_see_checks" {
  filename = "lambda_function_see_checks.zip"
  function_name = "prod_lambda_see_checks"
  role = var.aws_role
  handler = "see_checks.lambda_handler"
  runtime = "python3.6"
  publish = true
}

#Create a Lambda function for see all checks
resource "aws_lambda_function" "prod_lambda_see_all_checks" {
  filename = "lambda_function_see_all_checks.zip"
  function_name = "prod_lambda_see_all_checks"
  role = var.aws_role
  handler = "see_all_checks.lambda_handler"
  runtime = "python3.6"
  publish = true
}

#Create a Lambda function for upload face file
resource "aws_lambda_function" "prod_lambda_upload_face" {
  filename = "lambda_function_upload_face.zip"
  function_name = "prod_lambda_upload_face"
  role = var.aws_role
  handler = "upload_face.lambda_handler"
  runtime = "python3.6"
  publish = true
}

#############
## STORAGE ##
#############

# Create a S3 bucket for video uploads
resource "aws_s3_bucket" "video_bucket" {
  bucket = "video_bucket.faas.muii"
}

# Create a database with a timestamp and a person id
resource "aws_dynamodb_table" "processed_data_table" {
  name = "processed_data_table"
  attributes = {
    hash_key = "person_id"
    range_key = "timestamp"
    billing_mode = "PAY_PER_REQUEST"
  }
}
