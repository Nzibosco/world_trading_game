import re

from src.ai_trading.template_parsers.Action import Action


class Transfer(Action):

    def __init__(self, template_file_path):
        self.template_str = None
        self.from_country = None
        self.to_country = None
        self.resource = None
        self.quantity = None

        with open(template_file_path, 'r') as file:
            data = file.read().strip()
            self.template_str = data

        self.parse_transfer(data)

    def __str__(self):
        return self.template_str

    def parse_transfer(self, transfer_str):
        pattern = r'\(TRANSFER\s+(\w+)\s+(\w+)\s+\(\((\w+)\s+(\d+)\)\)\)'
        match = re.match(pattern, transfer_str)

        if match is not None:
            self.from_country = match.group(1)
            self.to_country = match.group(2)
            self.resource = match.group(3)
            self.quantity = int(match.group(4))

    def execute(self, world_state):
        pass

