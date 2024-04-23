# Function to read HTML file, replace placeholder, and return modified content
def render_html_template(template_path, **kwargs):
    # Read the contents of the HTML file
    with open(template_path, 'r') as file:
        html_content = file.read()

    # Replace placeholders with provided keyword arguments
    for key, value in kwargs.items():
        html_content = html_content.replace('{{ ' + key + ' }}', str(value))

    return html_content