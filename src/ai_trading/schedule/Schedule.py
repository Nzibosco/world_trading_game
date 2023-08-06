import os
from queue import PriorityQueue
from typing import List

from src.ai_trading.states.ResourceWeight import ResourceWeight
from src.ai_trading.states.WorldState import WorldState
from src.ai_trading.template_parsers.Action import Action
from src.ai_trading.template_parsers.Transfer import Transfer
from src.ai_trading.template_parsers.Transform import Transform
from src.ai_trading.utils import quality_score


def generate_actions(directory_path, logger) -> List[Action]:
    actions = []

    for filename in os.listdir(directory_path):
        # Make sure we're reading only txt files
        if filename.endswith(".txt"):
            template_path = os.path.join(directory_path, filename)
            with open(template_path, 'r') as file:
                contents = file.read().strip()

                if 'TRANSFER' in contents:
                    transfer_action = Transfer(template_path, logger)
                    actions.append(transfer_action)

                elif 'TRANSFORM' in contents:
                    transform_action = Transform(template_path, logger)
                    actions.append(transform_action)

    return actions


def output_schedules(best_schedules, output_schedule_filename):
    pass


class Schedule:
    def __init__(self, templates_path: str, resources_filename: str, initial_state_filename: str, logger):
        self.logger = logger

        self.actions = generate_actions(templates_path, logger)
        self.resource_weights = ResourceWeight(resources_filename)
        self.initial_state = WorldState(initial_state_filename)

    '''
    Country will use this agent to figure out the best schedule that maximize its state quality
    '''

    def country_scheduler(self, country_name, output_schedule_filename,
                          num_output_schedules, depth_bound,
                          frontier_max_size):

        initial_utility = quality_score.average_quality_score(self.initial_state, self.resource_weights)
        self.logger.debug(f'Initial Utility value is {initial_utility}')

        frontier = PriorityQueue(maxsize=frontier_max_size)
        frontier.put((-initial_utility, self.initial_state))  # Added depth info

        best_schedules = []

        while not frontier.empty():
            current_utility, current_state = frontier.get()  # Fetch depth info
            self.logger.debug(f'Got current utility {current_utility} from frontier. depth: {current_state.depth}')

            # If depth bound is reached
            if current_state.depth >= depth_bound:
                self.logger.debug(f'Examining state at depth {current_state.depth} with utility {current_utility}')
                print(current_state.schedule)
                best_schedules.append(current_state.schedule)
                if len(best_schedules) >= num_output_schedules:
                    break
                continue

            for action in self.actions:
                current_depth = current_state.depth
                new_state = action.execute(current_state)
                new_state.depth = current_depth + 1
                new_utility = quality_score.average_quality_score(new_state, self.resource_weights)

                # Add state to frontier if conditions are met
                if frontier.qsize() < frontier_max_size:
                    self.logger.debug(f'Adding new state in the frontier. current depth is {new_state.depth}. Utility= {new_utility}')
                    frontier.put((-new_utility, new_state))
                self.logger.debug('Done adding states for current run')

        # Output the schedules
        output_schedules(best_schedules, output_schedule_filename)

