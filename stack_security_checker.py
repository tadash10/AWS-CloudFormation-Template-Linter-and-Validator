import boto3

def check_security_best_practices(cf_client, stack_name, logical_resource_id):
    try:
        response = cf_client.detect_stack_drift(StackName=stack_name, LogicalResourceIds=[logical_resource_id])
        return response['StackResourceDrift']['DriftStatus'] == 'IN_SYNC'
    except Exception as e:
        print(f"An error occurred while checking drift for resource {logical_resource_id}: {str(e)}")
        return False
