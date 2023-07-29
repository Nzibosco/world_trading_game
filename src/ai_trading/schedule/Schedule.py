from queue import PriorityQueue

from src.ai_trading.states.WorldState import WorldState


def load_resources(resources_filename):
    pass


def load_initial_state(initial_state_filename):
    pass


def generate_actions(current_state, resources):
    pass


def apply_action(current_state, action):
    pass


def output_schedules(best_schedules, output_schedule_filename):
    pass


class Schedule:
    def __init__(self, schedule_id='SCD_1'):
        self.schedule_id = schedule_id
        self.templates = []
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
            self.deduct_inputs(world_state, template.country, template.inputs)
            self.add_outputs(world_state, template.country, template.outputs)
            print('Saving new state after executing action')
            world_state.save()

    '''
    This method is used to add TRANSFORM and TRANSFER operators to the schedule
    '''
    def add_template(self, template):
        self.templates.append(template)

    def deduct_inputs(self, world_state, country, inputs):

        for k, v in inputs.items():
            if k != 'Population':
                current_value = world_state.get_country_resource_qty(country, k)
                print(f'Current value for resource {k} in country {country} is {current_value}')
                # Check if input has right balance
                if current_value > v:
                    next_val = current_value - v
                    print(f'New value for {k} after executing this action is {next_val}')
                    world_state.update_country_resources(k, next_val, country)

    def add_outputs(self, world_state, country, outputs):
        for k, v in outputs.items():
            if k != 'Population':
                current_value = world_state.get_country_resource_qty(country, k)
                print(f'Current value for resource {k} in country {country} is {current_value}')
                next_val = current_value + v
                print(f'New value for {k} after adding new outputs {next_val}')
                world_state.update_country_resources(k, next_val, country)

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
        # Load resources -- Injecting world state obj gives all resources
        resources = load_resources(resources_filename)

        # Load initial state
        initial_state = load_initial_state(initial_state_filename)

        # Initialize a priority queue for the frontier
        # From python doc on heapq: The queue uses the negative of utility because heapq in Python is a min-heap
        frontier = PriorityQueue(maxsize=frontier_max_size)
        frontier.put((-initial_state.utility, initial_state))

        # Placeholder for best schedules found
        best_schedules = []

        # Explore the state space up to the depth-bound
        while not frontier.empty():
            # Take the state with the highest utility from the frontier
            _, current_state = frontier.get()

            # If we have reached the depth-bound, add the schedule to the best schedules
            if current_state.depth >= depth_bound:
                best_schedules.append(current_state.schedule)

                # If we have found enough schedules, break
                if len(best_schedules) >= num_output_schedules:
                    break

                continue

            # Generate new states by applying actions
            for action in generate_actions(current_state, resources):
                new_state = apply_action(current_state, action)

                # Add the new state to the frontier if it's not too large yet
                if frontier.qsize() < frontier_max_size or new_state.utility > -frontier.queue[0][0]:
                    frontier.put((-new_state.utility, new_state))

        # Output the schedules
        output_schedules(best_schedules, output_schedule_filename)
