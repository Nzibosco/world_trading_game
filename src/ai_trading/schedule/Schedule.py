import os
from typing import List

from src.ai_trading.states.ResourceWeight import ResourceWeight
from src.ai_trading.states.WorldState import WorldState
from src.ai_trading.template_parsers.Action import Action
from src.ai_trading.template_parsers.Transfer import Transfer
from src.ai_trading.template_parsers.Transform import Transform
from src.ai_trading.utils import quality_score
from src.ai_trading.utils.PriorityQueue import PriorityQueue


LINE_BREAK = '__________________________________________________________________________'


class Schedule:
    def __init__(self, templates_path: str, resources_filename: str, initial_state_filename: str, logger):
        self.logger = logger
        self.frontier = PriorityQueue()
        self.actions = self.generate_actions(templates_path)
        self.resource_weights = ResourceWeight(resources_filename)
        self.initial_state = WorldState(initial_state_filename)

    def generate_actions(self, directory_path) -> List[Action]:
        actions = []

        for filename in os.listdir(directory_path):
            # Make sure we're reading only txt files
            if filename.endswith(".txt"):
                template_path = os.path.join(directory_path, filename)
                with open(template_path, 'r') as file:
                    contents = file.read().strip()

                    if 'TRANSFER' in contents:
                        transfer_action = Transfer(template_path, self.logger)
                        actions.append(transfer_action)

                    elif 'TRANSFORM' in contents:
                        transform_action = Transform(template_path, self.logger)
                        actions.append(transform_action)

        return actions

    '''
    Country will use this agent to figure out the best schedule that maximize its state quality
    '''

    def country_scheduler(self, country_name, output_schedule_filename,
                          num_output_schedules, depth_bound,
                          frontier_max_size):

        initial_utility = quality_score.average_quality_score(self.initial_state, self.resource_weights)
        self.logger.debug(f'Initial Utility value is {initial_utility}')

        self.frontier.push(self.initial_state, initial_utility)  # Added depth info

        best_schedules = []

        while not self.frontier.is_empty():
            self.logger.debug(LINE_BREAK)
            current_state, current_utility = self.frontier.pop()  # Fetch depth info
            self.logger.debug(f'Started processing state with utility {current_utility}. depth: {current_state.depth}')

            if current_state.depth >= depth_bound or len(best_schedules) >= num_output_schedules:
                self.logger.debug(f'Max depth-bound or num schedules reached. Winding down...')
                self.logger.debug(LINE_BREAK)
                break

            if len(current_state.schedule) > 0:
                best_schedules.append((current_state.schedule, current_utility))

            # Increment the depth to keep track of it
            current_state.depth += 1

            for action in self.actions:
                # Add state to frontier if conditions are met
                if self.frontier.size() < frontier_max_size:
                    new_state = action.execute(current_state)
                    new_utility = quality_score.average_quality_score(new_state, self.resource_weights)
                    self.logger.debug(f'Adding new state in the frontier. current depth is {new_state.depth}. Utility= {new_utility}')
                    self.frontier.push(new_state, new_utility)
                else:
                    self.logger.debug('Could not add more states. Allowed frontier max size reached.')
            self.logger.debug('Done adding states for current run')

        # Output the schedules
        self.output_schedules(country_name, best_schedules, output_schedule_filename)

    def output_schedules(self, country_name, best_schedules, output_schedule_filename):
        self.logger.info(f'Printing best schedules for country {country_name} to a file...')
        with open(output_schedule_filename, 'w') as file:
            for schedule, utility in best_schedules:
                file.write("[\n")
                for action in schedule:
                    file.write(f"({action.__str__()}) \n")
                file.write(f"                                  EU: {utility}\n]\n")
        self.logger.info(f'Done writing best schedules for country {country_name} to {output_schedule_filename}')



