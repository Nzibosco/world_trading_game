from src.ai_trading.states.WorldState import WorldState


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
