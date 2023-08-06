from src.ai_trading.schedule.Schedule import Schedule
from src.ai_trading.states.ResourceWeight import ResourceWeight
from src.ai_trading.states.WorldState import WorldState
from src.ai_trading.utils.ai_logger import app_logger


def add_new_resource(world_state:WorldState, resource_weight: ResourceWeight, resource_name, column_loc, values, weight):
    print("Adding new resources to the csv files...")
    world_state.add_resource(resource_name, column_loc, values)
    resource_weight.add_resource(resource_name, weight)
    print("Added new resource to the state and weights files.")


def app_driver(logger):
    logger.debug("Starting AI Powered World Trading Game...")

    logger.info("Creating A schedule from Action Templates...")
    schedule: Schedule = Schedule('./templates', './resources/resource_weights.csv', "./resources/world_state.csv", logger)

    schedule.country_scheduler('Boscoland', 'output_schedule.txt', 5, 7, 5)


if __name__ == "__main__":
    ai_logger = app_logger("app_logs")  # Configuring logger and a log file
    app_driver(ai_logger)

    
