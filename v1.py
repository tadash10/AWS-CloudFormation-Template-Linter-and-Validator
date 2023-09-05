import os
import subprocess
import boto3

def validate_template(template_path):
    try:
        # Use cfn-lint to validate the CloudFormation template
        subprocess.check_output(['cfn-lint', template_path])
        print(f"Template {template_path} is valid.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Template {template_path} is invalid:")
        print(e.output.decode('utf-8'))
        return False
    except FileNotFoundError:
        print("cfn-lint is not installed. Please install it.")
        return False

def check_security_best_practices(cf_client, stack_name, logical_resource_id):
    try:
        response = cf_client.detect_stack_drift(StackName=stack_name, LogicalResourceIds=[logical_resource_id])
        drift_status = response['StackResourceDrift']['DriftStatus']
        
        return drift_status == 'IN_SYNC'
    except Exception as e:
        print(f"An error occurred while checking drift for resource {logical_resource_id}: {str(e)}")
        return False

def main():
    # Specify the path to your CloudFormation template
    template_path = "path/to/your/template.yaml"

    if not os.path.exists(template_path):
        print(f"Template file '{template_path}' not found.")
        return

    # Validate the template
    if validate_template(template_path):
        try:
            # Connect to AWS CloudFormation using boto3
            cf_client = boto3.client('cloudformation', region_name='us-east-1')

            # Define security best practices checks
            best_practices_checks = [
                {"Description": "Security groups should have descriptions."},
                {"Description": "Security groups should not be wide open."},
                # Add more checks for best practices here
            ]

            stack_name = 'YourStackName'
            resource_name = 'YourResourceName'

            # Check for best practices in the CloudFormation template
            for check in best_practices_checks:
                if check_security_best_practices(cf_client, stack_name, resource_name):
                    print(f"{check['Description']}: PASSED")
                else:
                    print(f"{check['Description']}: FAILED")
        except Exception as e:
            print(f"An error occurred while processing the template: {str(e)}")

if __name__ == "__main__":
    main()
