import argparse

from src.ai_trading.schedule.Schedule import Schedule
from src.ai_trading.utils.ai_logger import app_logger


def parse_arguments():
    parser = argparse.ArgumentParser(description="AI Powered World Trading Game Driver")

    # Define the command-line arguments
    parser.add_argument("--templates_path", default="./templates", help="Path to action templates directory.")
    parser.add_argument("--resources_weights_path", default="./resources/resource_weights.csv", help="Path to resource weights CSV file.")
    parser.add_argument("--world_state_path", default="./resources/world_state.csv", help="Path to world state CSV file.")
    parser.add_argument("--country_name", default="Boscoland", help="Name of the country for scheduling.")
    parser.add_argument("--output_schedule_filename", default="output_schedule.txt", help="Filename for output schedules.")
    parser.add_argument("--num_output_schedules", type=int, default=5, help="Number of output schedules to generate.")
    parser.add_argument("--depth_bound", type=int, default=7, help="Depth bound for the scheduling process.")
    parser.add_argument("--frontier_max_size", type=int, default=5, help="Maximum size of the frontier for the scheduling process.")

    # Parse and return the arguments
    return parser.parse_args()


def app_driver(args, logger):
    logger.debug("Starting AI Powered World Trading Game...")

    logger.info("Creating A schedule from Action Templates...")
    schedule: Schedule = Schedule(args.templates_path, args.resources_weights_path, args.world_state_path, logger)

    schedule.country_scheduler(args.country_name, args.output_schedule_filename, args.num_output_schedules, args.depth_bound, args.frontier_max_size)

    logger.debug("Execution completed. Exiting...")


if __name__ == "__main__":
    args = parse_arguments()  # Parse the command-line arguments

    ai_logger = app_logger("app_logs")  # Configuring logger and a log file
    app_driver(args, ai_logger)
