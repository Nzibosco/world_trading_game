# WORLD TRADING SCHEDULER
## AI Powered World Building and Trading Game 


## Description
This project aims to create optimized schedules for countries to maximize their state quality. By using certain economic actions and accounting for various resource weights, the project produces the most efficient schedule for a given country based on the provided depth-bound and frontier size.

Currently, the project support two types of actions:
- Transform 
- Transfer

## Transform 
A country transforms its raw resources into manufactured resources. It is important to note that this action can result in waste which negatively impact the state quality as presented in resource weight file. 

## Transfer
Transfer action occurs when country C1 transfers a certain amount of resource r to country c2.

## Requirements

- Python 3.8 or higher.
- Pandas library.
- Other dependencies: Refer to `requirements.txt`.

## Installation

1. Clone this repository:

        git clone https://github.com/Nzibosco/world_trading_game.git
2. Navigate to the cloned directory: 
        
        cd country-scheduler

3. Install the required dependencies:

        pip install -r requirements.txt 


## Usage

1. Ensure your data files are set up in the correct format.
2. Run the main script:

        python app.py --country_name "CountryName" --output_schedule_filename "output.txt" --num_output_schedules 10 --depth_bound 5 --frontier_max_size 100 
        
Replace the placeholders with your desired values.

## Structure

- **WorldState**: Represents the current state of the world, loaded from a file.
- **ResourceWeight**: Handles the weights of different resources.
- **Schedule**: Central class that handles the scheduling logic.
  - `generate_actions`: Generates available actions from templates.
  - `country_scheduler`: Determines the best schedules.
  - `output_schedules`: Outputs the best schedules to a file.

## Future Improvements

1. **Parallel Execution**: Explore parallel execution techniques to speed up the scheduling process.
2. **Data Visualization**: Integrate visualization tools to provide insights into how schedules impact country metrics.
3. **Heuristic Enhancements**: Investigate the possibility of integrating machine learning techniques for better utility score predictions.
4. **Transfer Action Handshake**: Have each country running on a separate thread and real time handshake between two countries involved in transfer action.

## Contributing

Pull requests are welcome. Please ensure your PR passes all tests before submitting. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

Thanks to my classmates and faculty members at Vanderbilt University, School of Engineering and the developers who have contributed to this project.


