terraform {
 required_providers {
   aws = {
     source = "hashicorp/aws"
   }
 }
}
    
provider "aws" {
  region  = "eu-west-1"
  profile = "dynamodb-simple-json-api"
}