module "stop_instances" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "stop_instances"
  description   = "Python Lambda function for stopping running EC2 instances that match a specific string."
  handler       = "main.lambda_handler"
  runtime       = "python3.13"
  source_path = {
    path = "../src",
    patterns = [
      "!__pycache__/?.*",
    ]
  }
  architectures            = ["arm64"]
  attach_policy_statements = true
  policy_statements = {
    ec2 = {
      effect    = "Allow",
      actions   = ["ec2:DescribeInstances", "ec2:StopInstances"],
      resources = ["*"]
    },
  }
  cloudwatch_logs_retention_in_days = 7
}