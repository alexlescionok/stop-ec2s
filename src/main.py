import json
from functions import get_instances, stop_instances

def lambda_handler(event: dict, context) -> dict:
    """The main Lambda handler function
    
    Parameters
    ----------
    event: dict
        Dictionary containing the Lambda function event data
    context: awslambdaric.lambda_context.LambdaContext
        Lambda runtime context
    
    Returns
    ----------
    operation_status: the dictionary with information on operation success/failure.
    """

    try:
        if "StringToMatch" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "success": False,
                    "error": "Missing required parameter: 'StringToMatch'"
                })
            }
        string_to_match = event["StringToMatch"]
        instances = get_instances(string_to_match)
        if instances:
            result = stop_instances(instances)
            if result["success"]:
                print(f"Successfully stopped the following instances: {instances}")
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "success": True,
                        "message": f"Successfully stopped {len(result['stopped_instances'])} instance(s)",
                        "stoppedInstances": result['stopped_instances']
                    })
                }
            elif result["error"]:
                print(f"Failed to stop instance(s). Error: {result['error']}")
                return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "success": False,
                        "error": result["error"] 
                    })
                }
        else:
            print(f"No running instances with names that include '{string_to_match}'. Ending operation here.")
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "success": True,
                    "message": f"No running instances with names that include '{string_to_match}'. Ending operation here."
                })
            }
    except Exception as e:
        print(e)