from template_validator import validate_cloudformation_template
from aws_connector import connect_to_aws_cloudformation
from stack_security_checker import check_security_best_practices
from file_loader import load_template_path

def run_security_checks(cf_client, stack_name, resource_name, best_practices_checks):
    try:
        for check in best_practices_checks:
            if check_security_best_practices(cf_client, stack_name, resource_name):
                print(f"{check['Description']}: PASSED")
            else:
                print(f"{check['Description']}: FAILED")
    except Exception as e:
        print(f"An error occurred while running security checks: {str(e)}")

def main():
    template_path = load_template_path()

    if template_path and validate_cloudformation_template(template_path):
        cf_client = connect_to_aws_cloudformation('us-east-1')
        if cf_client:
            stack_name = 'YourStackName'
            resource_name = 'YourResourceName'

            best_practices_checks = [
                {"Description": "Security groups should have descriptions."},
                {"Description": "Security groups should not be wide open."},
                # Add more checks for best practices here
            ]

            run_security_checks(cf_client, stack_name, resource_name, best_practices_checks)

if __name__ == "__main__":
    main()
