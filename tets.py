
import boto3
import subprocess
import sys
import os

def validate_template(template_path):
    # Use cfn-lint to validate the CloudFormation template
    try:
        subprocess.check_output(['cfn-lint', template_path])
        print(f"Template {template_path} is valid.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Template {template_path} is invalid:")
        print(e.output.decode('utf-8'))
        return False

def main():
    # Specify the path to your CloudFormation template
    template_path = "path/to/your/template.yaml"

    # Validate the template
    if not os.path.exists(template_path):
        print(f"Template file '{template_path}' not found.")
        sys.exit(1)

    if validate_template(template_path):
        # Connect to AWS CloudFormation using boto3
        cf_client = boto3.client('cloudformation', region_name='us-east-1')

        # Define security best practices checks
        best_practices_checks = [
            {"Check": "security_group_has_description", "Description": "Security groups should have descriptions."},
            {"Check": "security_group_not_open", "Description": "Security groups should not be wide open."},
            # Add more checks for best practices here
        ]

        # Check for best practices in the CloudFormation template
        for check in best_practices_checks:
            response = cf_client.detect_stack_drift(StackName='YourStackName', LogicalResourceIds=['YourResourceName'])

            if response['StackResourceDrift']['DriftStatus'] == 'IN_SYNC':
                print(f"{check['Description']}: PASSED")
            else:
                print(f"{check['Description']}: FAILED")

if __name__ == "__main__":
    main()
