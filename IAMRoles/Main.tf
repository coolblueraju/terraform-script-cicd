terraform {
	required_providers {
		aws = {
			source = "hashicorp/aws"
		}
	}

 backend "s3" {
    bucket = "terraform-backend-datastore-23012023"
    key    = "global/iamrole/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
	region = "us-east-1"
}