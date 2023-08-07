from src.ai_trading.states.ResourceWeight import ResourceWeight
from src.ai_trading.states.WorldState import WorldState


def add_new_resource(world_state: WorldState, resource_weight: ResourceWeight, resource_name, column_loc, values, weight):
    """
    This function is used to dynamically update the world_state file
    """
    print("Adding new resources to the csv files...")
    world_state.add_resource(resource_name, column_loc, values)
    resource_weight.add_resource(resource_name, weight)
    print("Added new resource to the state and weights files.")