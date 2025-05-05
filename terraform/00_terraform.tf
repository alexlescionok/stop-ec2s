locals {
  default_region = "REPLACE_ME"
  default_tags = {
    /*
    Default tags you wish to apply across all resources provisioned by terraform, for example:
    environment = "production"
    project     = "core-components"
    */
  }
}

terraform {

  required_version = "~> 1.11.0"

  backend "s3" {
    bucket = "lescionok-terraform-state"
    region = "eu-west-1"
    key    = "stop-ec2s"

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
  region                   = local.default_region
  shared_config_files      = ["$HOME/.aws/config"]
  shared_credentials_files = ["$HOME/.aws/credentials"]
  profile                  = "REPLACE_ME"
  default_tags {
    tags = local.default_tags
  }
}