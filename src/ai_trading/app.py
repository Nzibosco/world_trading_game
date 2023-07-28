from src.ai_trading.schedule.Schedule import Schedule
from src.ai_trading.states.RescourceWeight import ResourceWeight
from src.ai_trading.states.WorldState import WorldState
from src.ai_trading.template_parsers.Transfer import Transfer
from src.ai_trading.template_parsers.Transform import Transform
from src.ai_trading.utils import quality_score


def add_new_resource(world_state:WorldState, resource_weight: ResourceWeight, resource_name, column_loc, values, weight):
    print("Adding new resources to the csv files...")
    world_state.add_resource(resource_name, column_loc, values)
    resource_weight.add_resource(resource_name, weight)
    print("Added new resource to the state and weights files.")


def app_driver():
    print("Starting AI Powered World Trading Game...")

    print("Creating Initial World State...")
    world_state: WorldState = WorldState("./resources/world_state.csv")

    print("Loading Resource Weight file")
    resource_weights: ResourceWeight = ResourceWeight('./resources/resource_weights.csv')

    print("Initial World State: ")
    print(world_state.countries)

    print("Creating A schedule from Action Templates...")
    schedule: Schedule = Schedule()

    print("Loading templates from files ... ")
    electronics_template: Transform = Transform('./templates/electronics_template.txt')
    housing_template: Transform = Transform('./templates/housing_template.txt')
    print(housing_template.outputs)
    housing_transfer: Transfer = Transfer('./templates/housing_transfer.txt')
    print(housing_transfer)
    print("Created some templates. Adding to the schedule ...")
    schedule.add_template(electronics_template)
    schedule.add_template(housing_template)
    print("Added Templates to the Schedule.")

    print(f"Initial World State Quality Before Executing the Schedule:: {quality_score.average_quality_score(world_state, resource_weights)}")

    print("About to execute the schedule")
    schedule.execute_schedule(world_state)

    print("New State After executing the schedule")
    print(world_state.countries)

    print(f"World Quality Score after executing the schedule:: {quality_score.average_quality_score(world_state, resource_weights)}")

    print("Restoring World State After....")
    schedule.restore_init_state(world_state)
    print(world_state.df)


if __name__ == "__main__":
    app_driver()
