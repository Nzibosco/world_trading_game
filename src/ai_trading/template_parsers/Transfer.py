import copy
import re

from src.ai_trading.template_parsers.Action import Action


class Transfer(Action):

    def __init__(self, template_file_path, logger):
        with open(template_file_path, 'r') as file:
            data = file.read().strip()
            self.template_str = data
        self.logger = logger
        self.from_country = None
        self.to_country = None
        self.resource = None
        self.quantity = None
        self.parse_transfer(data)

        super().__init__(self.from_country)

    def __str__(self):
        return self.template_str

    def parse_transfer(self, transfer_str):
        pattern = r'\(TRANSFER\s+(\w+)\s+(\w+)\s+\(\((\w+)\s+(\d+)\)\)\)'
        match = re.match(pattern, transfer_str)

        if match:
            self.from_country = match.group(1)
            self.to_country = match.group(2)
            self.resource = match.group(3)
            self.quantity = int(match.group(4))
        else:
            self.logger.error(f"Unable to parse transfer string: {transfer_str}")

    def execute(self, world_state):
        # Create a deep copy of the input world_state
        new_world_state = copy.deepcopy(world_state)

        self.logger.debug(f'Executing Transfer Action between countries {self.from_country} and {self.to_country}')

        resource_qty = new_world_state.get_country_resource_qty(self.from_country, self.resource)
        resource_qty_to = new_world_state.get_country_resource_qty(self.to_country, self.resource)

        self.logger.info(f'Country {self.from_country} has qty {resource_qty} of resource {self.resource}')

        if resource_qty >= self.quantity:
            self.logger.info(f'Transferring {self.quantity} of {self.resource} to {self.to_country}')

            new_qty_from = resource_qty - self.quantity
            new_qty_to = resource_qty_to + self.quantity

            new_world_state.update_country_resources(self.resource, new_qty_from, self.from_country)
            new_world_state.update_country_resources(self.resource, new_qty_to, self.to_country)
            new_world_state.schedule.append(self)
        else:
            self.logger.warning('Not enough resources. Could not execute Transfer action.')
        self.logger.debug(f'Done executing Transfer Action')
        return new_world_state
