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
  stream_view_type = "NEW_IMAGE"
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

resource "awscc_rekognition_collection" "rekognition_collection" {
  collection_id = "rekognition_collection"
  
}


# Shared values to work with Serverless
resource "aws_ssm_parameter" "dynamo_arn" {
  name = "dynamo-table-stream-param"
  type = "String"
  value = aws_dynamodb_table.processed_data_table.stream_arn
}

resource "aws_ssm_parameter" "s3_name_param" {
  name = "s3-arm-param"
  type = "String"
  value = aws_s3_bucket.video-bucket-faas-muii.na
}


resource "aws_ssm_parameter" "rekognition_collection_param" {
  name = "rekognition-collection-param"
  type = "String"
  value = awscc_rekognition_collection.rekognition_collection.collection_id

}

resource "aws_ssm_parameter" "topic_param" {
     name = "topic-arn-param"
     type = "String"
     value = aws_sns_topic.email_topic.arn
}