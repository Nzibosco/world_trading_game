import re

class Transform:
    def __init__(self, file_path):
        self.transform_template = file_path
        self.template_str = None
        self.country = None
        self.inputs = None
        self.outputs = None

        with open(self.transform_template, 'r') as file:
            data = file.read()
            self.template_str = data
        self.parse_template(data)

    def __str__(self):
        return self.template_str

    def parse_template(self, template_string):
        # split the template into lines
        lines = template_string.split("\n")

        self.inputs = {}
        self.outputs = {}
        self.country = ''
        current_section = None

        for line in lines:
            # remove leading and trailing whitespaces
            line = line.strip()

            if line.startswith('(TRANSFORM'):
                # get the country code
                self.country = line.split(' ')[1]
            elif line.startswith('(INPUTS'):
                current_section = 'INPUTS'
            elif line.startswith('(OUTPUTS'):
                current_section = 'OUTPUTS'
            elif line.startswith('(') and line.endswith(')') and current_section is not None:
                # extract the key and value from the line
                match = re.match(r'\((\w+)\s(\d+)\)', line)
                if match:
                    key, value = match.groups()
                    if current_section == 'INPUTS':
                        self.inputs[key] = int(value)
                    else:
                        self.outputs[key] = int(value)

# Usage:
# transformation = Transform('../templates/electronics_template.txt')
# print(transformation.country)
# print(transformation.inputs)
# print(transformation.outputs)
# print(transformation.transform_template)
