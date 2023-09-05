import os

def load_template_path():
    template_path = "path/to/your/template.yaml"

    if not os.path.exists(template_path):
        print(f"Template file '{template_path}' not found.")
        return None

    return template_path
