import os
from queue import PriorityQueue
from typing import List

from src.ai_trading.states.ResourceWeight import ResourceWeight
from src.ai_trading.states.WorldState import WorldState
from src.ai_trading.template_parsers.Action import Action
from src.ai_trading.template_parsers.Transfer import Transfer
from src.ai_trading.template_parsers.Transform import Transform
from src.ai_trading.utils import quality_score


def load_resources(resources_filename):
    pass


def load_initial_state(initial_state_filename):
    pass


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



def apply_action(current_state, action):
    pass


def output_schedules(best_schedules, output_schedule_filename):
    pass


class Schedule:
    def __init__(self, template_path: str, logger, schedule_id='SCD_1'):
        self.logger = logger
        self.schedule_id = schedule_id
        self.templates = generate_actions(template_path, logger)
        self.actions = self.templates

        self.initial_state = None

    '''
    Method takes in word_state object and adjust resources depending on action operator. 
    For example, if we manufacture 5 houses, the corresponding country's resources will be adjusted 
    to reflect resources taken out and newly created ones.
    '''
    def execute_schedule(self, world_state: WorldState):
        # Currently working with TRANSFORM templates alone as we are dealing with one currently
        print(f'Schedule {self.schedule_id} will execute {len(self.templates)} actions')

        self.initial_state = world_state.df.copy(deep=True)
        print(self.initial_state)
        for template in self.templates:
            print(f'executing.... {template.country}')
            template.execute(world_state)
            print('Saving new state after executing action')
            #world_state.save()

    '''
    This method is used to add TRANSFORM and TRANSFER operators to the schedule
    '''
    def add_template(self, template):
        self.templates.append(template)

    def restore_init_state(self, world_state: WorldState):
        if self.initial_state is not None:
            print('Restoring initial state')
            world_state.df = self.initial_state
            world_state.save()


    '''
    Country will use this agent to figure out the best schedule that maximize its state quality
    '''
    def country_scheduler(self, country_name, resources_filename,
                          initial_state_filename, output_schedule_filename,
                          num_output_schedules, depth_bound,
                          frontier_max_size):

        # Load initial state
        initial_state: WorldState = WorldState(initial_state_filename)

        # Ressource weights
        resource_weights: ResourceWeight = ResourceWeight(resources_filename)
        utility = quality_score.average_quality_score(initial_state, resource_weights)
        self.logger.debug(f'Initial Utiliy value is {utility}')

        # Initialize a priority queue for the frontier
        # From python doc on heapq: The queue uses the negative of utility because heapq in Python is a min-heap
        frontier = PriorityQueue(maxsize=frontier_max_size)
        frontier.put((-utility, initial_state))

        # Placeholder for best schedules found
        best_schedules = []

        # Explore the state space up to the depth-bound
        while not frontier.empty():

            # Take the state with the highest utility from the frontier
            _, current_state = frontier.get()

            # If we have reached the depth-bound, add the schedule to the best schedules
            if len(self.actions) >= depth_bound:
                best_schedules.append(current_state.schedule)

                # If we have found enough schedules, break
                if len(best_schedules) >= num_output_schedules:
                    break

                continue

            # Generate new states by applying actions
            for action in self.actions:
                new_state = action.execute(current_state)

                # Add the new state to the frontier if it's not too large yet
                utility = quality_score.average_quality_score(new_state, resource_weights)
                if frontier.qsize() < frontier_max_size or utility > -frontier.queue[0][0]:
                    frontier.put((-utility, new_state))

        # Output the schedules
        output_schedules(best_schedules, output_schedule_filename)
