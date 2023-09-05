import subprocess

def validate_cloudformation_template(template_path):
    try:
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
