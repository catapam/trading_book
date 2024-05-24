# Trading Book System

[Live project can be viewed here](https://trading-book-de510f70748d.herokuapp.com/)

The Trading Book System is an open-source interactive command-line tool designed to help users manage and track their trading activities. Key features include logging trades, updating settings, viewing current statistics, and seamless integration with Google Sheets for data storage and retrieval.

![flowchart](documentation/flowchart.png)

# Table of Contents

* [Description](#description)
* [User Experience](#user-experience)
    * [User Story](#user-story)
* [Design](#design)
* [Features](#features)
    * [Existing Features](#existing-features)
    * [Future Features](#future-features)
* [How to Use](#how-to-use)
    * [Example of Valid Commands](#example-of-valid-commands)
* [Error Handling](#error-handling)
    * [Initialization Errors](#initialization-errors)
    * [Read and Write Operations](#read-and-write-operations)
    * [User Input Validation](#user-input-validation)
    * [Confirmation and Navigation](#confirmation-and-navigation)
* [Technology Used](#technology-used)
    * [Language](#language)
    * [Frameworks, Libraries and Programs](#frameworks-libraries-and-programs)
* [Deployment](#deployment)
* [Testing](#testing)
    * [Manual Testing](#manual-testing)
* [Bugs](#bugs)
* [Future optimizations](#future-optimizations)
* [Credits](#credits)
    * [Code](#code)
    * [Content](#content)
* [Acknowledgements](#acknowledgements)

# User Experience

The Trading Book System is designed with the user in mind, providing a clear and structured interface for managing trades. Users can easily input trade data, view current settings, and check the status of their trades. The system ensures data integrity and provides helpful feedback, making it a reliable tool for both novice and experienced traders.

## User Story

As a trader, I want to be able to log my trades efficiently, update my trading settings, and view my current trades and statistics, so that I can manage my trading activities effectively.

# Design

The design of the Trading Book System is based on a flowchart that outlines the expected flow of operations, validation processes, and interactions with the Google Sheets database. This ensures a seamless user experience and efficient data management.

Key design principles include:
- **User-Centric Design**: Focused on providing clear prompts and feedback.
- **Modular Architecture**: Separation of concerns through different classes and methods.
- **Robust Error Handling**: Comprehensive error handling to ensure reliability.

Errors are displayed in red, and successes are displayed in green. Confirmations are required before moving away from any jobs or completing a new trade entry input.

# Features

* **Smart Input Interpreter**: Enhances user experience by simplifying data entry and minimizing errors. It processes and validates user inputs intelligently, ensuring correct formatting and alignment with system requirements. For example, the Entry function allows users to input data for other data requests within the same job. Confirmation requests are flexible, accepting variations like "YEAH" or "NOPE" in addition to simple "y/n" inputs.
* **Trade Entry**: Log new trades with details such as action, asset, type, price, stop, and ATR. Also allows bulk import by inputting JSON format according to specifications.
* **Settings Management**: Update and view settings such as position number, drawdown, and total risk. This feature currently serves as a showroom and does not affect trades but is prepared for future integrations.
* **Trade Check**: View current open trades and their statistics. Open trades guide future entries, ensuring no multiple trades are opened for the same asset. Close and update entries are only allowed on assets with an open trade.
* **Data Validation**: Ensures all inputs meet specified formats and constraints. The system handles data smartly, moving data around to fit correctly, and prompts the user for new data when auto-validation is not possible.
* **Help and Tips**: Accessible from any part of the code, the help function adjusts its content according to the current context, providing relevant instructions and tips.

## Future features

* **Advanced Analytics**: Integrate more advanced analytics for trade performance and risk management.
* **Automated Alerts**: Add functionality for automated alerts based on trade conditions identified.
* **Auto Execution of Trades**: Enable fully automated trading via API requests to stock exchanges.
* **Automate the whole trade chain of processes**: From pricing patterns reading to order execution at the exchagen, the full process can be automated. Alerts of moves can be sent via API to Telegram to keep the user up to date, while the program convert price patterns into money, by reading patterns, creating signals of entry and exit, position sizing, risk management, API call to communicate the new move and API call to execute the same at the exchange. Almost a whole Commodity Trading Fund. 
* **Work as an installed module on a Linux server**: Integrating the created functions with Bash commands can significantly enhance user capabilities. By allowing direct parsing through logs while interacting with the program, users can achieve a new level of control and efficiency in their workflows. Security, scalability and performance would be significantly improved in a setup like that.

# How to use

1. **Start the Application**: Run the main script to start the Trading Book System.
2. **Enter Commands**: Use the command line interface to enter commands for logging trades, updating settings, or checking current trades.
3. **Follow Prompts**: The system will prompt you for necessary inputs and provide feedback on actions taken.
4. **View Results**: Use the `check` command to view current open trades and their details.
5. **Type help**: Type help at any time to get insights on how to input the correct data or navigate around.

## Example of valid Commands

- **Logging a Trade**:
```
entry
./entry
entry type:short open
./entry open asset:spy short 50000 45000 atr:1%
entry asset:btc long 50000 stop:45000 3% open
```

* Updating Settings:
```
./set position:5 drawdown:10% risk:5%
set
```

* Checking Open Trades:
```
./check
```

* Help:
```
./help
help
./help entry
help ./set
help check
exit ./help
```

* Cancel:
```
./cancel
cancel
cancel y      (this one forces it thorugh without asking confirmation)
```

# Error handling

The Trading Book System includes robust error handling mechanisms to ensure that the application can gracefully handle and recover from various error scenarios. 

By implementing these error handling strategies, the Trading Book System ensures that users receive clear, informative feedback and that the application remains stable and reliable, even when unexpected situations occur.

Below are the key aspects of how error handling is managed in the system:

## Initialization Errors

During the initialization of the DataBaseActions class, several types of errors are caught and handled to ensure the system can provide informative feedback and maintain stability:

* DefaultCredentialsError: Occurs when the credentials file is not found or cannot be loaded. The system prints a message indicating the failure to load credentials.
* GoogleAuthError: Handles authentication failures with the Google API. An error message is displayed to inform the user.
* APIError: Catches issues related to the gspread client authorization. An appropriate error message is printed.
* General Exception: Any unexpected errors during initialization are caught and logged with a generic message.

## Read and Write Operations

Error handling is also implemented for read and write operations to ensure data integrity and provide clear feedback to the user:

* Read Errors: When reading data from a worksheet, the system catches APIError and general exceptions, printing an error message and returning None.
* Write Errors: When appending data to a worksheet, the system handles APIError and general exceptions similarly, ensuring users are informed if the write operation fails.

## User Input Validation

User input is validated through various methods to ensure correctness and provide meaningful error messages when invalid data is encountered:

* Format Validation: The system checks if inputs match the expected format using regular expressions. If validation fails, an error message is printed, and None is returned.
* Auto-Validation: Inputs that can be automatically validated are processed and corrected if possible. If validation fails, the user is prompted to re-enter the data.

## Confirmation and Navigation

The system ensures that before moving away from a current job or completing a new trade entry, the user is asked for confirmation:

* Confirmation Requests: The system uses a yes_or_no function to interpret various forms of affirmative and negative responses, ensuring flexibility in user input.

# Technology used

## Language

* Python

## Frameworks, Libraries and Programs

* **gspread**: For interacting with Google Sheets.
* **Google OAuth2**: For authentication and authorization with Google APIs.
* **json**: For handling JSON data.
* **datetime**: For managing date and time data.
* **re**: For allowing usage of regular expressions in format interpretation and validation.
* **[LucidChart](https://lucid.app)**: For flowchart creation and project initial planning.
* **Visual Studio Code**: As the integrated development environment (IDE) of choice.
* **Google Sheets**: Used as a database for storing and managing trade data. The project’s Google Sheet can be viewed [here](https://docs.google.com/spreadsheets/d/11yF7zZ4YkLPFGiV84rwFdnI6vDUi4uwlRiTczyG5f3U/edit?usp=sharing)
* **builtins and textwrap**: Used to fix text wrapper issues

# Deployment

The Code Institute Python Essentials Template was utilized for this project to ensure the Python code can be executed in a terminal within a browser.

To deploy the application on Heroku:

1. Visit the Heroku website, log in, or create a new account.
2. On the dashboard, click "New" and select "Create new app."
3. Enter a unique app name and choose a region.
4. Click "Create app."
5. Navigate to the "Settings" tab and find "Config Vars."
6. Click "Reveal Config Vars," add "PORT" as a key with the value "8000," and click "Add."
7. Scroll down to the "Buildpacks" section, click "Add buildpack," and select "Python."
8. Repeat step 7 to add "Node.js," ensuring "Python" is listed first.
9. Scroll to the top and select the "Deploy" tab.
10. Choose GitHub as the deployment method, then search for your repository and click "Connect."
11. Scroll down and either "Enable Automatic Deploys" to update the code each time it is pushed to GitHub, or choose "Manual Deploy" for manual updates.

# Testing

Testing was primarily conducted using the VSC (Visual Studio Code) terminal. Given the complexity of the code, testing and fixes were integrated into the development process. The project initially started with a set of loose functions and later transitioned to an object-oriented programming (OOP) structure for better management and readability.

PEP8 compliance was first ensured after completing the Entry feature, which was the initial significant feature of the program. From that point onward, each commit was only accepted if the code was 100% PEP8 compliant. This practice facilitated maintaining clean and standardized code throughout the development process.

Errors were identified early and addressed promptly, adhering to the daily work schedule. Dedicated testing time was allocated each day to ensure thorough validation. Inspired by the principles outlined in the "Clean Code" book, the primary objective for each function was to ensure functionality. Once the function was working correctly, optimizations were made to keep the code concise, well-commented, and easily maintainable.

## Manual testing

This is a command line project, all the manual testing was focused on checking valid commands, sucessful responses and error handling.

### Main menu and multi string inputs

| **Feature** | **CLI Input** | **Expected Result** | **Actual Result** |
|-------------|---------------|---------------------|-------------------|
| General | `""` | Similarly to known terminal flow, empty input simply ask a new input without showing any errors. This is intended for familiarity purposes |  Works as expected |
| General | `"   "` | Similarly to known terminal flow, blank input simply ask a new input without showing any errors. This is intended for familiarity purposes |  Works as expected |
| General | `"foobar"` | Invalid request error message and back to main input request |  Works as expected |
| Help | ```help``` | Open general help options and back to main input request |  Works as expected |
| Help | ```hepl``` | Invalid request error message and back to main input request | Works as expected |
| Help | ```Help entry``` | Fix capital letter to 'help', open entry help options and back to main input request | Works as expected |
| Help | ```help ./set``` | Takes help as priority request, open set help options (which shows current settings at the end) and back to main input request | Works as expected |
| Help | ```help help``` | Open general help options and back to main input request | Works as expected |
| Help | ```./help cancel``` | Help already takes priority over any menu requests, './' changes nothing on the behavior here, returns cancel help options and back to main input request | Works as expected |
| Help | ```./help ./exit``` | Help takes priority and shows exit help options, going back to main input request afterwards | Works as expected |
| Help | ```check help``` | Help takes priority and shows check help options, going back to main input request afterwards | Works as expected |
| Help | ```back ./help``` | Help takes priority and shows back help options, going back to main input request afterwards | Works as expected |
| Help | ```banana ./help``` | Error returns informing 'banana' is not a valid input, general help is shown, alert to try again and go back to main input request | Works as expected |
| Help | ```apple help``` | Error returns informing 'apple' is not a valid input, general help is shown, alert to try again and go back to main input request | Works as expected |
| Help | ```./apple help``` | Error returns informing 'apple' is not a valid input, general help is shown, alert to try again and go back to main input request | Works as expected |
| Help | ```help grape``` | Error returns informing 'grape' is not a valid input, general help is shown, alert to try again and go back to main input request | Works as expected |
| Help | ```help ./grape``` | Error returns informing 'grape' is not a valid input, general help is shown, alert to try again and go back to main input request | Works as expected |
| Help | ```./help entyr``` | Error returns informing 'entyr' is not a valid input, general help is shown, alert to try again and go back to main input request | Works as expected |
| Help | ```help ./entry set``` | Help takes priority over './entry' and 'set', './' forces entry through as secondary command, set is ignored, shows entry help options, going back to main input request afterwards | Works as expected |
| Help | ```help entry ./ste``` | ./ste is invalidated, shows entry help options, going back to main input request afterwards | Works as expected |
| Help | ```help entry ./check``` | Help takes priority over './check' and 'entry', './' forces check through as secondary command, entry is ignored, shows check help options, going back to main input request afterwards | Works as expected |
| Check | ```help ./entry ./check``` | Help takes priority over './entry' and './check', './' forces entry through as secondary command, './check' is ignored, shows entry help options, going back to main input request afterwards | Check help options is shown instead of entry help |
| Check | ```check``` | Open check options, showing a table with all open orders if there is any, or error if there is none and back to main input request | Works as expected |
| Check | ```chekc``` | Invalid request error message and back to main input request | Works as expected |
| Check | ```check ./entry``` | Entry takes priority over 'check' due to presence of forcing menu string './', shows entry options | Works as expected |
| Check | ```check help``` | Help takes priority and shows check help options, going back to main input request afterwards | Works as expected |
| Check | ```check banana``` | Error message is shown informing 'banana' is not a valid input, and plain check is run | 'banana' is ignored, and check function works ok, but no error message shown |
| Check | ```apple check``` | Error message is shown informing 'apple' is not a valid input, and plain check is run | 'apple' is ignored, and check function works ok, but no error message shown |
| Check | ```grape ./check``` | Error message is shown informing 'grape' is not a valid input, and plain check is run | 'grape' is ignored, and check function works ok, but no error message shown |
| Check | ```check set entry``` | Invalid request error message, being first string 'check' is taken as priority and run it and back to main input request | Works as expected |
| Check | ```check ./set entry``` | Invalid request error message, having './' string 'set' is taken as priority and run it and back to main input request | Works as expected |
| Check | ```check set ./entry``` | Invalid request error message, having './' string 'entry' is taken as priority and run it and back to main input request | Works as expected |
| Cancel | ```cancel``` | Request confirmation to cancel the current job, or inform there is nothing to cancel if no job is in progress | Works as expected |
| Cancel | ```cancle``` | Invalid request error message and back to main input request | Works as expected |
| Cancel | ```cancel ./entry``` | Entry takes priority over 'cancel' due to presence of './', starts entry options | Works as expected |
| Cancel | ```cancel help``` | Help takes priority and shows cancel help options, going back to main input request afterwards | Works as expected |
| Cancel | ```cancel banana``` | Error message is shown informing 'banana' is not a valid input, and plain cancel is run | 'banana' is being ignored, and cancel function works ok, but no error message shown |
| Cancel | ```apple cancel``` | Error message is shown informing 'apple' is not a valid input, and plain cancel is run | 'apple' is being ignored, and cancel function works ok, but no error message shown |
| Cancel | ```grape ./cancel``` | Error message is shown informing 'grape' is not a valid input, and plain cancel is run | 'grape' is being ignored, and cancel function works ok, but no error message shown |
| Cancel | ```cancel set entry``` | Invalid request error message, being first string 'check' is taken as priority and run it and back to main input request | Works as expected |
| Cancel | ```cancel ./set entry``` | Invalid request error message, having './' string 'set' is taken as priority and run it and back to main input request | Works as expected |
| Cancel | ```cancel set ./entry``` | Invalid request error message, having './' string 'entry' is taken as priority and run it | Works as expected |
| Cancel | ```cancel y``` | If a job is running, cancellation is self confirmed and proceeds without asking again | Works as expected |
| Cancel | ```cancel n``` | If a job is running, cancellation is self rejected and main input request is prompted again | Works as expected |
| Exit | ```exit``` | Exit the program after user confirmation | Works as expected |
| Exit | ```exti``` | Invalid request error message and back to main input request | Works as expected |
| Exit | ```exit ./entry``` | Invalid request error message, having './' string 'entry' is taken as priority and run it | Works as expected |
| Exit | ```exit help``` | Help takes priority and shows exit help options, going back to main input request afterwards | Works as expected |
| Exit | ```exit banana``` | 'banana' is invalidated showing error message, and exit is continued | 'banana' is being passed to exit showing the error message of invalid input on the confirmation request |
| Exit | ```apple exit``` | 'apple' is invalidated showing error message, and exit is continued | 'apple' is being passed to exit showing the error message of invalid input on the confirmation request |
| Exit | ```grape ./exit``` | 'grape' is invalidated showing error message, and exit is continued | 'grape' is being passed to exit showing the error message of invalid input on the confirmation request |
| Exit | ```exit set entry``` | Invalid request error message, being first string 'exit' is taken as priority, run it and back to main input request | Works as expected |
| Exit | ```exit ./set entry``` | Invalid request error message, having './' string 'set' is taken as priority and run it and back to main input request | Works as expected |
| Exit | ```exit set ./entry``` | Invalid request error message, having './' string 'entry' is taken as priority and run it and back to main input request | Works as expected |
| Exit | ```exit y``` | Exit is self confirmed and proceeds without asking again | Works as expected |
| Exit | ```exit n``` | Exit is self rejected and main input request is prompted again | Works as expected |
| Back | ```back``` | Go back to the previous menu if possible, or inform there is nowhere to go back to if already at the main menu | Works as expected |
| Back | ```bakc``` | Invalid request error message and back to main input request | Works as expected |
| Back | ```back ./entry``` | Invalid request error message, having './' string 'entry' is taken as priority and run it | Works as expected |
| Back | ```back help``` | Help takes priority and shows back help options, going back to main input request afterwards | Works as expected |
| Back | ```back banana``` | 'banana' is invalidated showing error message, and back is continued | 'banana' is ignored |
| Back | ```apple back``` | 'apple' is invalidated showing error message, and back is continued | 'apple' is ignored |
| Back | ```grape ./back``` | 'grape' is invalidated showing error message, and back is continued | 'grape' is ignored |
| Back | ```back set entry``` | Invalid request error message, being first string 'back' is taken as priority, run it and back to main input request | Works as expected |
| Back | ```back ./set entry``` | Invalid request error message, having './' string 'set' is taken as priority and run it and back to main input request | Works as expected |
| Back | ```back set ./entry``` | Invalid request error message, having './' string 'entry' is taken as priority and run it and back to main input request | Works as expected |
| Set | ```set``` | Open set options, allowing user to modify settings | Works as expected |
| Set | ```ste``` | Invalid request error message and back to main input request | Works as expected |
| Set | ```set ./entry``` | Invalid request error message, having './' string 'entry' is taken as priority and run it | Works as expected |
| Set | ```set help``` | Help takes priority and shows set help options, going back to main input request afterwards | Works as expected |
| Set | ```set banana``` | 'banana' is invalidated showing error message, and set is continued | 'banana' is ignored |
| Set | ```apple set``` | 'apple' is invalidated showing error message, and set is continued | 'apple' is ignored |
| Set | ```grape ./set``` | 'grape' is invalidated showing error message, and set is continued | 'grape' is ignored |
| Set | ```set back entry``` | Invalid request error message, being first string 'set' is taken as priority, run it and back to main input request | Works as expected |
| Set | ```entry ./set cancel``` | Invalid request error message, having './' string 'set' is taken as priority and run it | Works as expected |
| Set | ```entry exit ./set``` | Invalid request error message, having './' string 'set' is taken as priority and run it | Works as expected |
| Set | ```set position:15 drawdown:30% risk:20% amount:1000.00``` | Update settings with the provided values and confirm the update | Works as expected |
| Set | ```set position:20 drawdown:30% risk:0.20 amount:1000.00``` | Update settings with the provided values and confirm the update, 'risk:0.20' returns invalid value | Works as expected |
| Set | ```set risk:20% amount:1000.00``` | Update settings with the provided values and confirm the update | Works as expected |
| Set | ```set 0,20``` | Invalid request error message for '0,20', starts function set without passing invalid string | No error message showing |
| Set | ```set 20%``` | Invalid request error message for '20%', starts function set without passing invalid string | No error message showing |
| Entry | ```entry``` | Open entry options, allowing user to log a trade | Works as expected |
| Entry | ```entyr``` | Invalid request error message and back to main input request | Works as expected |
| Entry | ```set ./entry``` | Entry takes priority over './set', shows entry options, going back to main input request afterwards | Works as expected |
| Entry | ```entry help``` | Help takes priority and shows entry help options, going back to main input request afterwards | Works as expected |
| Entry | ```entry banana``` | Starts entry, showing the invalidated value 'banana' in an error message | Works as expected |
| Entry | ```apple entry``` | Starts entry, showing the invalidated value 'apple' in an error message | Works as expected |
| Entry | ```grape ./entry``` | Starts entry, showing the invalidated value 'grape' in an error message | Works as expected |
| Entry | ```entry back entry``` | Invalid request error message, being first string 'entry' is taken as priority, run it and back to main input request | Works as expected |
| Entry | ```back ./entry cancel``` | Invalid request error message, having './' string 'entry' is taken as priority and run it| Works as expected |
| Entry | ```set exit ./entry``` | Invalid request error message, having './' string 'entry' is taken as priority and run it| Works as expected |
| Entry | ```entry bulk``` | Initiate bulk mode for trade entries | Works as expected |
| Entry | ```entry bulk [{"action":"open", "asset":"btc", "type":"long", "price":"15.00000000", "stop":"10.00000000", "atr":"0.0100"},{"action":"close", "asset":"btc", "type":"long", "price":"17.00000000", "stop":"13.00000000", "atr":"0.0110"}]``` | Although this is a valid JSON entry for bulk import, the string will always be invalidated at this point and requested inside the bulk menu options, avoiding potential wrong entries | Works as expected |
| Entry | ```entry bulk short``` | Initiates entry in bulk mode, showing error for any other parameters | Because short is a valid entry for one of the input requests the value is not showing on errors but just being ignored |
| Entry | ```entry bulk yada``` | Initiates entry in bulk mode, showing error for any other parameters | Works as expected |
| Entry | ```entry open bulk``` | Initiates entry in bulk mode, showing error for any other parameters | Because open is a valid entry for one of the input requests the value is not showing on errors but just being ignored |
| Entry | ```entry banana short asset:apple 1% 15 25 open``` | Invalid request error message for 'banana' reorder and validate the other paramaters and execute entry | Works as expected |
| Entry | ```entry open asset:apple short 15.50 25 1%``` | Reorder and validate the paramaters and execute entry | Works as expected |
| Entry | ```entry open apple short stop:15,50 25 0.01``` | Error Ivalidated data: ['apple', '0.01'], reorder and validate all the other paramenters, fixes 15,50 to 15.5 and execute entry function | Works as expected |
| Entry | ```entry action: close``` | Invalid request error message for 'action:', space separator is used incorrectly, as close is auto validable the action is still set to close and entry function executed | Works as expected |
| Entry | ```entry action:close asset:apple``` | Reorder and validate the paramaters and execute entry | Works as expected |
| Entry | ```entry 0,20``` | Fix ',' to '.' and validate the number value to the price which is the first number format accepted | Works as expected |
| Entry | ```entry 20%``` | Validate the % value to the atr which is the only % format accepted | Works as expected |


### Set inner functions

Running commands from inside 'set' function.

| **Feature** | **CLI Input** | **Expected Result** | **Actual Result** |
|-------------|---------------|---------------------|-------------------|
| General | "any input, except the next ones" | Invalid input error message, reprint the current settings and ask for new input | Works as expected |
| Multiple menu call | e.g. ```check entry``` | Invalid input error, 'check' takes priority and gets executed | Error message is printing twice |
| Multiple menu call | e.g. ```check ./entry``` | Invalid input error, 'entry' takes priority due to './' and gets executed | Error message is printing twice |
| Main menu call | ```help``` | Prints 'set' help options | Works as expected |
| Main menu call | ```help entry``` | Prints 'entry' help options | Works as expected |
| Main menu call | ```help invalid``` | 'invalid' is invalidated and return error message, Prints main help options | Works as expected |
| Main menu call | ```check``` | Open check options, showing a table with all open orders if there is any, or error if there is none and back to set input request | Works as expected |
| Main menu call | ```check banana``` | Error message is shown informing 'banana' is not a valid input, and plain check is run | 'banana' is ignored, and check function works ok, but no error message shown |
| Main menu call | ```exit``` | Alert that any non-saved data will be lost and ask confirmation before proceeding | Works as expected |
| Main menu call | ```exit n``` | Null command, it should only re-print the current settings and request for new input | Error message alerting data non-saved will be lost is being printed |
| Main menu call | ```exit x``` | Incorrect passed value to 'exit' function, error message and request for new confirmation on the exit command | Works as expected |
| Main menu call | ```exit y``` | Forced exit, no request for confirmation, just alerts the possibility of losing non-saved data and proceed | Works as expected |
| Main menu call | ```cancel``` | Alert that any non-saved data will be lost and ask confirmation before proceeding | Works as expected |
| Main menu call | ```cancel n``` | Null command, it should only re-print the current settings and request for new input | Works as expected |
| Main menu call | ```cancel x``` | Incorrect passed value to 'cancel' function, error message and request for new confirmation on the cancel command | Works as expected |
| Main menu call | ```cancel y``` | Forced cancel, no request for confirmation, just alerts the possibility of losing non-saved data and proceed | Works as expected |
| Main menu call | ```back``` | Alert that any non-saved data will be lost and ask confirmation before proceeding | Works as expected |
| Main menu call | ```back n``` | Null command, it should only re-print the current settings and request for new input | Works as expected |
| Main menu call | ```back x``` | Incorrect passed value to 'back' function, error message and request for new confirmation on the back command | Works as expected |
| Main menu call | ```back y``` | Forced back, no request for confirmation, just alerts the possibility of losing non-saved data and proceed | Works as expected |
| Main menu call | ```entry``` | Alert that any non-saved data will be lost and ask confirmation before proceeding, set will remain open, in case the user uses back or cancel on entry function | Works as expected |
| Main menu call | ```entry n``` | Null command, it should only re-print the current settings and request for new input | Works as expected |
| Main menu call | ```entry y``` | Forced entry, no request for confirmation, just alerts the possibility of losing non-saved data and proceed, value 'y' is also passed to entry | Works as expected |
| Main menu call | ```entry short``` | Alert that any non-saved data will be lost and ask confirmation before proceeding, passes 'short' to entry function | Works as expected |
| Main menu call | ```entry y short``` | Forced entry, no request for confirmation, just alerts the possibility of losing non-saved data and proceed, passes 'y short' to entry function where 'y' will be invalidated | Works as expected |
| Update settings | ```20``` | Invalid request error message, reprint input request | Works as expected |
| Update settings | ```position:18``` | Update setting position on the database and program output | Works as expected |
| Update settings | ```position:apple``` | Invalid request error message, reprint input request | Works as expected |
| Update settings | ```drawdown:0.35``` | Update setting drawdown to 35%(0.35) on the database and program output | Works as expected |
| Update settings | ```drawdown:35%``` | Update setting drawdown to 35%(0.35) on the database and program output | Works as expected |
| Update settings | ```drawdown:0,32``` | Fixes ',' to '.' and update setting drawdown to 32%(0.32) on the database and program output | Works as expected |
| Update settings | ```drawdown:pear``` | Invalid request error message, reprint input request | Works as expected |
| Update settings | ```risk:0.35``` | Update setting risk to 35%(0.35) on the database and program output | Works as expected |
| Update settings | ```risk:35%``` | Update setting risk to 35%(0.35) on the database and program output | Works as expected |
| Update settings | ```risk:0,32``` | Fixes ',' to '.' and update setting risk to 32%(0.32) on the database and program output | Works as expected |
| Update settings | ```risk:pear``` | Invalid request error message, reprint input request | Works as expected |
| Update settings | ```amount:1200.00``` | Update setting amount to 35%(0.35) on the database and program output | Works as expected |
| Update settings | ```amount:200%``` | Invalid request error message, reprint input request |  Update setting amount to 200%(2) on the database and program output |
| Update settings | ```amount:1200,00``` | Fixes ',' to '.' and update setting amount to 32%(0.32) on the database and program output | Works as expected |
| Update settings | ```amount:pear``` | Invalid request error message, reprint input request | Works as expected |

### Entry inner functions

Running commands from inside 'entry' function.

| **Feature** | **CLI Input** | **Expected Result** | **Actual Result** |
|-------------|---------------|---------------------|-------------------|
| General | "any input, except the next ones" | Invalid input error message, reprint the current settings and ask for new input | Works as expected |
| Multiple menu call | e.g. ```check entry``` | Invalid input error, 'check' takes priority and gets executed | Error message is printing twice |
| Multiple menu call | e.g. ```check ./entry``` | Invalid input error, 'entry' takes priority due to './' and gets executed | Error message is printing twice |
| Main menu call | ```help``` | Prints 'set' help options | Works as expected |
| Main menu call | ```help entry``` | Prints 'entry' help options | Works as expected |
| Main menu call | ```help invalid``` | 'invalid' is invalidated and return error message, Prints main help options | Works as expected |
| Main menu call | ```check``` | Open check options, showing a table with all open orders if there is any, or error if there is none and back to set input request | Works as expected |
| Main menu call | ```check banana``` | Error message is shown informing 'banana' is not a valid input, and plain check is run | 'banana' is ignored, and check function works ok, but no error message shown |
| Main menu call | ```exit``` | Alert that any non-saved data will be lost and ask confirmation before proceeding | Works as expected |
| Main menu call | ```exit n``` | Null command, it should only re-print the current settings and request for new input | Error message alerting data non-saved will be lost is being printed |
| Main menu call | ```exit x``` | Incorrect passed value to 'exit' function, error message and request for new confirmation on the exit command | Works as expected |
| Main menu call | ```exit y``` | Forced exit, no request for confirmation, just alerts the possibility of losing non-saved data and proceed | Works as expected |
| Main menu call | ```cancel``` | Alert that any non-saved data will be lost and ask confirmation before proceeding | Works as expected |
| Main menu call | ```cancel n``` | Null command, it should only re-print the current settings and request for new input | Works as expected |
| Main menu call | ```cancel x``` | Incorrect passed value to 'cancel' function, error message and request for new confirmation on the cancel command | Works as expected |
| Main menu call | ```cancel y``` | Forced cancel, no request for confirmation, just alerts the possibility of losing non-saved data and proceed | Works as expected |
| Main menu call | ```back``` | Alert that any non-saved data will be lost and ask confirmation before proceeding | Works as expected |
| Main menu call | ```back n``` | Null command, it should only re-print the current settings and request for new input | Works as expected |
| Main menu call | ```back x``` | Incorrect passed value to 'back' function, error message and request for new confirmation on the back command | Works as expected |
| Main menu call | ```back y``` | Forced back, no request for confirmation, just alerts the possibility of losing non-saved data and proceed | Works as expected |
| All parameters still required | Initial screen | Show help for entry and request first input for action | Works as expected |
| All parameters still required | ```bulk``` | Introductory message advise entry mode has been initiated, with example of input and input request | Works as expected |
| All parameters still required | ```bulk anything``` | Bulk is  priorityzed (except if main menu input): Introductory message advise entry mode has been initiated, with example of input and input request | Works as expected |
| All parameters still required | ```bulk set``` | Set is priorityzed and bulk ignored | Works as expected |
| All parameters still required | ```open``` or ```close``` or ```update``` | Action is updated on line above input request and move to next input request | Works as expected |
| All parameters still required | ```open short``` or any other number of valid input for other entry parameters | Action is updated, and short is defined as type on line above input request and move to next input request. Order of inputs is irrelevant, entry validations are smart to move them around and validate them if correctly requested | Works as expected |
| All parameters still required | ```open shot``` or any other number of invalid secondary input for other entry parameters | Action is updated on line above input request, 'shot' is invalidated and shows error message, and move to next input request. | Works as expected |
| All parameters still required | ```open asset:btc``` or any other number of valid input for other entry parameters using format key:value | Action and asset is updated on line above input request and move to next input request. As asset acepts any characteres and format types this can only be validated if key:value format is used | Works as expected |
| Action is defined | ```btc short``` or any other number of valid secondary input for other entry parameters | As asset is actively being requested the first input is identified as asset and all others try to validate against parameters not defined | Works as expected |
| Action is defined | ```btc close``` or any other number of valid secondary input for other entry parameters already defined | As asset is actively being requested the first input is identified as asset and all others try to validate against parameters not defined, in this case action was already defined so close is not validated and returns an error informing it | Works as expected |
| Action is defined | ```btc action:close``` or any other number of valid secondary input using format key:value for other entry parameters already defined | As asset is actively being requested the first input is identified as asset and all others try to validate against parameters not defined, in this case action was already defined but the format key:value is used, the edit is validated correctly | Works as expected |
| Action is defined as open and there is an open trade for asset called 'btc' | ```btc``` | Error message advising the asset already has an open order and cannot have duplicates | Works as expected |
| Action is defined as open and there is an open trade for asset called 'btc' | ```eth``` | Validates asset as normal and proceed | Works as expected |
| Action is defined as 'close' or 'update' and there is no open trade for asset called 'btc' | ```btc``` | Error message advising an order can only be closed or updated if there is an open order already | Works as expected |
| Action is defined as 'close' or 'update' and there is open trade for asset called 'btc' | ```btc``` | Validates as expected and continue | Works as expected |
| Other input requests | invalid values | Return error advising the invalidated value and ask same input again | Works as expected |
| Other input requests | valid values | Updates string above input request and move to next missing input | Works as expected |
| All inputs are completed | n/a | Requests confirmation of input data, if confirmed: complete showing a confirmation message and saves input on database | Works as expected |
| All inputs are completed | n/a | Requests confirmation of input data, if not confirmed: Error message and cancel | Works as expected |
| Bulk mode | invalid value | Error message and cancel | Works as expected |
| Bulk mode | ```[{"action":"open", "asset":"btc", "type":"long", "price":"15.00000000", "stop":"10.00000000", "atr":"0.0100"},{"action":"close", "asset":"btc", "type":"log", "price":"17.00000000", "stop":"13.00000000", "atr":"0.0110"}]``` | Validates each and every entry showing confirmation of passed input of error for invalid inputs | Works as expected |

# Bugs

Due to project delivery deadline some bugs were not fixed just yet, as they would demand quite some time on re-writting key functions, possibly requiring more testing. The small bugs found on testing phase do not affect the main functionality of the project or cause it to crash, being mostly related to layered loops causing duplicated error messages on specific situations. Adding some IF statements to filter those situations can resolve the issues, but again, demands time and testing.

Below it is a table of the tests that shown bugs, where the bugs are explained on the 'Actual result' column:

| **Feature** | **CLI Input** | **Expected Result** | **Actual Result** |
|-------------|---------------|---------------------|-------------------|
| Help Command Handling | `help ./entry ./check` | Help takes priority over './entry' and './check', './' forces entry through as secondary command, './check' is ignored, shows entry help options, going back to main input request afterwards. | Check help options are shown instead of entry help. |
| Check Command Error Handling | `check banana` | Error message is shown informing 'banana' is not a valid input, and plain check is run. | 'banana' is ignored, and check function works, but no error message is shown. |
| Check Command Error Handling | `apple check` | Error message is shown informing 'apple' is not a valid input, and plain check is run. | 'apple' is ignored, and check function works, but no error message is shown. |
| Check Command Error Handling | `grape ./check` | Error message is shown informing 'grape' is not a valid input, and plain check is run. | 'grape' is ignored, and check function works, but no error message is shown. |
| Cancel Command Error Handling | `cancel banana` | Error message is shown informing 'banana' is not a valid input, and plain cancel is run. | 'banana' is ignored, and cancel function works, but no error message is shown. |
| Cancel Command Error Handling | `apple cancel` | Error message is shown informing 'apple' is not a valid input, and plain cancel is run. | 'apple' is ignored, and cancel function works, but no error message is shown. |
| Cancel Command Error Handling | `grape ./cancel` | Error message is shown informing 'grape' is not a valid input, and plain cancel is run. | 'grape' is ignored, and cancel function works, but no error message is shown. |
| Exit Command Error Handling | `exit banana` | 'banana' is invalidated showing error message, and exit is continued. | 'banana' is passed to exit showing the error message of invalid input on the confirmation request. |
| Exit Command Error Handling | `apple exit` | 'apple' is invalidated showing error message, and exit is continued. | 'apple' is passed to exit showing the error message of invalid input on the confirmation request. |
| Exit Command Error Handling | `grape ./exit` | 'grape' is invalidated showing error message, and exit is continued. | 'grape' is passed to exit showing the error message of invalid input on the confirmation request. |
| Set Command Value Passing | `amount:200%` | Invalid request error message, reprint input request. | Update setting amount to 200%(2) on the database and program output. |

# Future optimizations

Over the course of nearly 200 hours dedicated to this project, numerous objects and functions were created with reusability in mind. A significant portion of the code was designed to be reusable in other features or projects. However, some objects contain multiple methods and would benefit from being broken down into smaller, more manageable objects.

The manual testing section above show some issues on input requests, those need to be dealt with yet. Documenting it here for future updates reference.

Additionally, some functions currently perform multiple tasks. Due to time constraints, these functions had to be left as they are. This section of the README file has been included to highlight areas for future refactoring and improvement. Reworking these functions and objects will enhance code modularity, readability, and maintainability.

# Credits

## Code

* **gspread**: For interacting with Google Sheets.
* **Google OAuth2**: For authentication and authorization.
* **[Code Institute's PEP8 validator](https://pep8ci.herokuapp.com/)**: For reviewing code formatting for PEP8 validation.
* **[Black](https://pypi.org/project/black/)**: For reviewing code formatting for PEP8 validation.
* **[Clean Code in Python](https://www.amazon.co.uk/Clean-Code-Python-maintainable-efficient)**: As a reference for maintainable and efficient Python coding.

## Content

* **[ChatGPT](https://chat.openai.com/)**: For text reviews and copywriting assistance.

# Acknowledgements

* **Gareth Mc Girr**: My mentor, for all the help and advice throughout the project.
* **Code Institute**: For all the training and guidance.
* **WP Engine**: My current employer, for providing all the support necessary and allowing great networking.
