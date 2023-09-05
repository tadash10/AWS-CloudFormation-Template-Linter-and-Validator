import boto3

def connect_to_aws_cloudformation(region_name):
    try:
        return boto3.client('cloudformation', region_name=region_name)
    except Exception as e:
        print(f"Failed to connect to AWS CloudFormation: {str(e)}")
        return None
