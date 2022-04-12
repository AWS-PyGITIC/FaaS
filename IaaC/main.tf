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


#EC2 with the trained model
resource "aws_instance" "vm_1" {
  ami = "ami-0b0af3577fe5e3532" #RHEL ami
  instance_type = "t2.micro"
  subnet_id = aws_subnet.prod_subnet-1.id

  tags = {
    Name = "RHEL"
  }

}

