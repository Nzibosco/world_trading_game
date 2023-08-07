from src.ai_trading.schedule.Schedule import Schedule
from src.ai_trading.utils.ai_logger import app_logger


def app_driver(logger):
    logger.debug("Starting AI Powered World Trading Game...")

    logger.info("Creating A schedule from Action Templates...")
    schedule: Schedule = Schedule('./templates', './resources/resource_weights.csv',
                                  "./resources/world_state.csv", logger)

    schedule.country_scheduler('Boscoland', 'output_schedule.txt', 5, 7, 5)

    logger.debug("Execution completed. Exiting...")


if __name__ == "__main__":
    ai_logger = app_logger("app_logs")  # Configuring logger and a log file
    app_driver(ai_logger)

