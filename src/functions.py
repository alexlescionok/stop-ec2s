import boto3

ec2_client = boto3.client('ec2')

# Including pagination to reduce the chance of throttling and timeouts 
paginator = ec2_client.get_paginator('describe_instances')

def get_instances(string_to_match: str) -> list:
    """A function that finds running EC2 instances that include the provided string in their name. 
    
    Parameters
    ----------
    string_to_match: str
        The string that the function will match against running EC2 instances.
    
    Returns
    ----------
    running_instances: the list of EC2 IDs.
    """
    try:
        page_iterator = paginator.paginate(
            Filters = [
                {
                    'Name': 'instance-state-code',
                    'Values': ['16']
                },
                {
                    'Name': 'tag:Name',
                    'Values': [f'*{string_to_match}*']
                }
            ],
            PaginationConfig = {'MaxItems': 10}
        )
        running_instances = []
        for page in page_iterator:
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    running_instances.append((instance['InstanceId']))
        
        print(f"Found the following running instances with names that include '{string_to_match}': {running_instances}")
        return running_instances
    except Exception as e:
        print(f"Error describing instances: {str(e)}")
        return []

def stop_instances(instances: list) -> dict:
    """A function that stops EC2 instances that are provided in the list.
    
    Parameters
    ----------
    instances: list
        The string that the function will match against running EC2 instances.
    """
    try:
        print(f"Attempting to stop the following running instances: {instances}")
        response = ec2_client.stop_instances(InstanceIds=instances)
        return {
            "success": True,
            "stopped_instances": [instance["InstanceId"] for instance in response.get("StoppingInstances", [])]
        }
    except Exception as e:
        print(f"Error stopping instances: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }