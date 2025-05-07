# stop-ec2s
Python AWS Lambda for stopping running EC2 instances.

## Table of Contents

- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [CI/CD](#cicd)
- [License](#license)

## Project Overview
This project provisions a Python AWS Lambda that allows users to stop running EC2 instances that match a supplied string. The project uses Terraform for infrastructure management, and is continuously tested and deployed through GitHub Actions.

## Requirements
- Python 3.x
- Terraform 1.11
- boto3
- pytest
- pytest-mock
- AWS Account (with proper access rights)

## Installation
### Clone the Repository
```bash
git clone https://github.com/alexlescionok/stop-ec2s.git
cd stop-ec2s
```

## Usage
The AWS Lambda is triggered by an event. For example, to stop running EC2 instances that match the string "testing", pass the following object: `{"StringToMatch": "testing"}`. This can be triggered manually or by other AWS services, for example, Amazon EventBridge.

## Running Tests
The Python code can be tested using pytest.
```bash
pytest --maxfail=0
```

## CI/CD
The project uses GitHub Actions to test, validate, and deploy the AWS Lambda function (and related AWS infrastructure). The project comes with two workflows: `ci-pull-request.yml` and `cd-merge.yml`. The workflows rely on the following repository secrets to be set: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. If these are not included, the workflows will be unable to interact with AWS. 

### Continuous Integration
The `ci-pull-request.yml` workflow runs during pull requests that include changes to the `src`, `tests`, or `terraform` directories, and ensures that:
- Linting is performed via Ruff.
- Pytest runs tests.
- Terraform validates, formats, and produces a plan.

### Continuous Deployment
The `cd-merge.yml` workflow runs when a pull request with changes to the `src`, `tests`, or `terraform` directories is merged into the `main` branch. When this happens, the workflow applies the Terraform code.

## License
This project is licensed under the [MIT License](LICENSE).