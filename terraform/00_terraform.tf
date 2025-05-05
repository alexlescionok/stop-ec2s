locals {
  default_tags = {
    environment = "test"
    project     = "github-actions-testing"
  }
}

terraform {

  required_version = "~> 1.11.0"

  backend "s3" {
    bucket = "lescionok-terraform-state"
    region = "eu-west-1"
    key    = "github-actions-testing/stop-ec2s"

    encrypt      = true
    use_lockfile = true
  }


  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.97.0"
    }
  }
}

### Default provider
provider "aws" {
  default_tags {
    tags = local.default_tags
  }
}