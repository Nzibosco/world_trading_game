import copy
import re

from src.ai_trading.states.WorldState import WorldState
from src.ai_trading.template_parsers.Action import Action


def add_pairs(line, current_dict):
    pairs = re.findall(r'\((\w+)\s(\d+)\)', line)
    for pair in pairs:
        key, value = pair
        current_dict[key] = int(value)


def deduct_inputs(world_state: WorldState, country, inputs, logger):

    for k, v in inputs.items():
        if k != 'Population':
            current_value = world_state.get_country_resource_qty(country, k)
            logger.info(f'Current value for resource {k} in country {country} is {current_value}')
            # Check if input has right balance
            if current_value > v:
                next_val = current_value - v
                logger.info(f'New value for {k} after executing this action is {next_val}')
                world_state.update_country_resources(k, next_val, country)


def add_outputs(world_state: WorldState, country, outputs, logger):
    for k, v in outputs.items():
        if k != 'Population':
            current_value = world_state.get_country_resource_qty(country, k)
            logger.info(f'Current value for resource {k} in country {country} is {current_value}')
            next_val = current_value + v
            logger.info(f'New value for {k} after adding new outputs {next_val}')
            world_state.update_country_resources(k, next_val, country)


class Transform(Action):
    def __init__(self, file_path, logger):
        self.logger = logger
        self.transform_template = file_path
        self.template_str = None
        self.country = None
        super().__init__(self.country)
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
                # Add any inputs on the same line
                add_pairs(line, self.inputs)
            elif line.startswith('(OUTPUTS'):
                current_section = 'OUTPUTS'
                # Add any outputs on the same line
                add_pairs(line, self.outputs)
            elif line.startswith('(') and line.endswith(')') and current_section is not None:
                # extract the key and value from the line
                match = re.match(r'\((\w+)\s(\d+)\)', line)
                if match:
                    key, value = match.groups()
                    if current_section == 'INPUTS':
                        self.inputs[key] = int(value)
                    else:
                        self.outputs[key] = int(value)

    def execute(self, world_state):
        self.logger.debug(f'Executing Transform Action for country {self.country}...')
        # Create a deep copy of the input world_state
        new_world_state = copy.deepcopy(world_state)
        deduct_inputs(new_world_state, self.country, self.inputs, self.logger)
        add_outputs(new_world_state, self.country, self.outputs, self.logger)
        new_world_state.schedule.append(self)
        self.logger.debug(f'Done executing Transform Action')
        return new_world_state

