# WORLD TRADING SCHEDULER
## AI Powered World Building and Trading Game 


## Description
This project aims to create optimized schedules for countries to maximize their state quality. By using certain economic actions and accounting for various resource weights, the project produces the most efficient schedule for a given country based on the provided depth-bound and frontier size.

## Project structure 

Below picture shows the project structure and where to locate files

![Project structure](https://user-images.githubusercontent.com/46146669/258677768-402407bf-7da8-400d-a0ff-d4632891a086.png)

* Resource folder contains raw csv files representing initial world state and resource weight 
* templates folder contains txt files representing transform and transfer operations. 
* template parsers include classes for parsing and representing actions in templates.
* schedule folder contains main logic for the scheduler and utils folder has a custom Priority Queue that was used for identifying best schedules.

Currently, the project support two types of actions:
- Transform 
- Transfer

### Transform 
A country transforms its raw resources into manufactured resources. It is important to note that this action can result in waste which negatively impact the state quality as presented in resource weight file. 
Refer to templates package to see the format.

### Transfer
Transfer action occurs when country C1 transfers a certain amount of resource r to country c2.
Refer to templates package for formatting.

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

Depending on your python environment, you can also use a multiline command as shown below: 

        python app.py --templates_path ./templates
              --resources_weights_path ./resources/resource_weights.csv
              --world_state_path ./resources/world_state.csv
              --country_name Boscoland
              --output_schedule_filename output_schedule.txt
              --num_output_schedules 5
              --depth_bound 7
              --frontier_max_size 5 

**Note**: Please make sure you have the latest version of python installed. If you experience issues running the project from command line, please use IDE such as PyCharm and run ''app.py'' file. 
Once the script is run, you will see output file in the destination you set. 
Additionally, default arguments have been provided just in case. 

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

More info soon.

## Acknowledgments

Thanks to my classmates and faculty members at Vanderbilt University, School of Engineering and the developers who have contributed to this project.


