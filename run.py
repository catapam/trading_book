import gspread
import re
from google.oauth2.service_account import Credentials


# Define the Google API scopes that the application will need access to.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('trading_book')


##Styling
class StyleOutput:
    """
    Provides methods to print messages with various ANSI escape code based styles. This class simplifies the
    process of applying text styles such as colors, bold, and underline in console outputs.

    Attributes:
        styles (dict): A dictionary mapping style names to their corresponding ANSI escape codes.
    """
    styles={"red":"\033[31m",
            "green":"\033[32m",
            "cyan":"\033[96m",
            "gray":"\033[2m",
            "orange":"\033[1m\033[38;5;208m",
            "bold":"\033[1m",
            "italic":"\033[3m",
            "dim":"\033[2m",
            "underscore":"\033[4m",
            "none":"\033[0m",
            "title":"\n\n\n\033[1m\033[32m   ",
            "green_background":"\033[1m\033[42m\033[97m",
            "error":"\033[1m\033[41m\033[97m"
            }

    @classmethod
    def apply_style(cls,style_name):
        """
        Applies the specified style to a message.

        Args:
            style_name (str): The name of the style to apply. Must be a key in the `styles` dictionary.

        Returns:
            function: A function that takes a message as an argument and returns the styled message.
        """
        def styled_message(message):
            return f"{cls.styles[style_name]}{message}{cls.styles['none']}"
        return styled_message


#General atributes
styles = StyleOutput()
GREETING = styles.apply_style('orange')
TITLE = styles.apply_style('title')
PATH = styles.apply_style('gray')
QUESTION = styles.apply_style('cyan')
SUCCESS= styles.apply_style('green_background')
ERROR= styles.apply_style('error')
red = styles.apply_style('red')
green = styles.apply_style('green')
bold = styles.apply_style('bold')
italic = styles.apply_style('italic')
underscore = styles.apply_style('underscore')
dim = styles.apply_style('dim')   

main_menu=["entry","set","check","exit","help","cancel","back"]
# main_menu = list(MainMenu.command.keys())

##General Functions
def get_input(prompt):
    """
    Prompts the user for input and returns the sanitized input as a lowercase string with leading and trailing whitespace removed.

    This function is crucial for interacting with the user, collecting input directly from the command line interface. 
    It ensures that the input is consistently formatted to facilitate further processing without concerns about 
    case sensitivity or extraneous whitespace.

    Args:
        prompt (str): The message displayed to the user, indicating what information is being requested.

    Returns:
        str: The user's input, converted to lowercase and stripped of any leading or trailing whitespace.
             This normalization helps in simplifying further command processing and comparisons.

    Example:
        If the user types '  Yes  ' in response to a prompt, this function will return 'yes', 
        removing the leading/trailing spaces and converting to lowercase, which is particularly 
        useful for standardized input processing in command-driven applications.
    """
    # Display the prompt to the user, formatted with a question style
    user_input = input(QUESTION(f"{prompt}"))

    # Return the input after stripping whitespace and converting to lowercase
    return user_input.strip().lower()
           

def delete_none_values(trade_details,num):
    """
    Filters out None values from a specified field in a dictionary of details.

    This function is useful for cleaning data by removing None entries from a collection
    of information before further processing or display. It ensures that only
    valid, non-None data is kept for subsequent operations.

    Args:
        trade_details (dict): A dictionary where each key is an identifier and each value
                              is a tuple (or list) containing data.
        num (int): The index in the tuple or list from each dictionary value that should be 
                   checked for None values.

    Returns:
        list: A list of values extracted from the specified index in each tuple or list of the 
              dictionary's values, excluding any None values.

    The function navigates through the dictionary, accesses the specified index of each tuple,
    and builds a list of these values, excluding any that are None. This is particularly useful
    in data processing where missing values need to be omitted from the output.
    """
    # Extract values from the specified index in each tuple or list in the dictionary values
    trade_values = [value[num] for value in trade_details.values()]

    # Convert each non-None value to string and compile into a list
    filtered_trade_values = [str(item) for item in trade_values if item is not None]
    
    return filtered_trade_values    


def yes_or_no(input):
    """
    Processes a user's response to a yes-or-no question, ensuring that the input is recognized
    and correctly interpreted as an affirmative or negative answer.

    This function is essential for confirmation dialogs where a user must explicitly agree or disagree
    with an action, such as exiting a program or deleting a file. It will continuously prompt the user
    until a valid response ('y' or 'n') is provided.

    Args:
        input (str): The initial user input to be evaluated.

    Returns:
        bool: True if the user's response is affirmative ('yes'), False if negative ('no').

    The function recognizes a variety of informal affirmations and negations to accommodate different
    user input styles.
    """
    # Dictionary of valid yes and no responses for broader acceptance of user input
    affirmative = {'y', 'yes', 'yeap', 'yeah', 'ya', 'ye', 'yy', 'yees', 'yess', 'sure', 'absolutely', 'indeed'}
    negative = {'n', 'no', 'nope', 'nah', 'not', 'dont', 'nn', 'nno', 'noo', 'never'}

    while True:
        if input in affirmative:
            return True
        elif input in negative:
            return False
        else:
            # Inform the user of invalid input and request a valid response
            print(ERROR("\nPlease use 'y' or 'n'."))
            input = get_input("\nEnter response:\n")
            continue


def pro_tips():
    """
    Displays professional tips for using the command line interface more effectively. These tips are aimed
    at helping users understand how to utilize various commands, handle input data, and navigate the application
    efficiently.

    The function outlines several key aspects:
    - Priority of commands, especially how 'help' is processed.
    - How to use the './' prefix to explicitly call menu commands.
    - The importance of correct data entry and how the system handles complex command strings.
    - Guidance on using advanced features like chaining subcommands or specifying data types explicitly.
    """
    # Introduce the section with an underlined and green-colored title
    print(underscore(green("\nPro tips:")))
    
    # Explain the hierarchical importance of the 'help' command
    print("- 'help' will always take priority over any other commands")
    print("- Typing 'help' followed by another command will provide more details on that command")
    print(dim("  Example: 'help entry'"))

    # Suggest starting with simple commands for newcomers
    print("- Allow some learning curve, and execute single commands at first")

    # Describe how to explicitly initiate main menu commands
    print("- Adding './' to the start of a string forces it to be checked as main menu call")
    print(dim("  Example: './entry"))

    # Provide examples on chaining commands and skipping ahead in workflows
    print("- You can also chain subcomands and skip steps ahead")
    print(dim("  Example: './entry open short'"))

    # Detail how the system prompts for missing data during operations
    print("- When running a job, you will be asked any missing data.")

    # Explain data input handling and validation
    print("- If any data is requested, you can see all the data already input just above the command request")
    print(dim("  Example: './entry open short' will appear just above the input request after running this command"))
    print("- When inputting data you can use multiple strings on any order, the data will try validate it correctly")
    print(dim("  Example: 'short ./entry open' or 'short entry open' will still work"))

    # Discuss forced data validation for specific subcommands
    print("- You can force data to be validated against a specific subcommand")
    print(dim("  Example: 'short ./entry action:open' or 'entry type:short open'"))

    # Highlight the requirement for declaring data types for certain entries
    print("- Some data entries like 'asset:' in './entry' MUST be declared with it's data type")
    print(dim("  Example: 'short ./entry asset:SPY open', where 'SPY' alone would be invalid, but ok as 'asset:SPY'"))

    # Illustrate how excess data input is managed
    print("- Too much data input will be handled by validating what can be validated first in the order of entries and delete others")
    print(dim("  Example: 'short ./entry asset:SPY long', 'type' will be set to 'short' and 'long' will be removed as both are 'type'"))

    # Explain how to update data once a subcommand is defined
    print("- After some subcommand is defined, editting it can be done by inputting a forced declaration")
    print(dim("  Example: current validated data is './entry asset:SPY type:short', entering 'type:long' will update the previously set value"))


# Validations start
class InputValidation:
    """
    Provides mechanisms to validate and process user inputs within a command-line interface.
    This class serves as a parser and interpreter for user commands, supporting complex command
    structures including context-based help and command extraction from mixed inputs.

    Attributes:
        input (str): User input string to be parsed and validated.
        context (str, optional): Contextual information or the current state of the application
                                 that may affect input processing.
    """
    def __init__(self, input,context=None):
        """
        Initializes the InputValidation instance with user input and optional context.

        Args:
            input (str): Raw user input string.
            context (str, optional): Contextual information relevant to input processing.
        """
        self.input=input
        self.context=context


    def remove_help_options(self, words):
        """
        This method processes a list of input words, identifies, and removes any that are specifically
        designated as help commands ('help' or './help'). It is designed to detect if help-related options
        are present in the user's command input and then exclude these specific tokens from the list. 
        This helps in distinguishing when the user is asking for help versus issuing other commands.

        Args:
            words (list of str): A list of words from the user's input that needs to be checked for 
                                help-related keywords.

        Returns:
            tuple: A tuple containing:
                - A string ('help' if any help-related keywords were found, empty string otherwise),
                indicating whether help was requested.
                - The list of words after removing any help-related keywords, which can be further processed
                by other command handling functions.

        Details:
        - The method defines a set of keywords that trigger help actions: {'help', './help'}.
        - It then filters these keywords out from the list of words, preserving only those that are not
        explicitly related to help commands.
        - The method checks if any of the help-related keywords were in the original list of words and
        returns 'help' if found, indicating that subsequent command processing should handle a help request.
        - This allows other parts of the command processing system to adapt their behavior based on whether
        help has been requested without having to re-check the input themselves.

        Example Usage:
        - Input: ['please', 'help', 'me']
        Output: ('help', ['please', 'me'])
        Here, 'help' is identified and removed, and the presence of a help request is confirmed.
        """
        # Define the keywords that are recognized as requests for help
        help_options = {'help', './help'}

        # Filter out the help keywords from the list of words
        no_help_words = []

        # Check if any help keywords were in the original words list
        no_help_words[:] = [word for word in words if word not in help_options]

        # Return both whether help was detected and the cleaned list of words
        return 'help' if any(option in words for option in help_options) else '', no_help_words


    def extract_command(self, words):
        """
        Extracts a command that starts with './', removing the prefix and identifying
        the command for processing.

        Args:
            words (list of str): A list of words from which to extract the command.

        Returns:
            tuple: The extracted command without './' prefix and the updated list of words.
        """
        for i in range(len(words) - 1, -1, -1):
            if words[i].startswith("./"):
                possible_command = words[i][2:]
                if possible_command in main_menu:
                    words.pop(i)
                    return possible_command, words
        return "",words


    def finalize_commands(self, words, parent_command):
        """
        Determines the final structure of the command and any child commands after initial processing.

        Args:
            words (list of str): Remaining words after removing known commands.
            parent_command (str): The initially determined parent command.

        Returns:
            tuple: The finalized parent command and a list of child commands.
        """
        child_command = []
        for word in words:
            if word in main_menu:
                if not parent_command:
                    parent_command = word
                elif parent_command == "help" and not child_command:
                    child_command = word
                else:
                    self.print_command_error(word, parent_command, child_command)
            else:
                child_command.append(word)
        return parent_command, child_command


    def print_command_error(self, word, parent_command, child_command):
        """
        Displays error messages for command conflicts, typically when multiple main commands
        are requested simultaneously.

        Args:
            word (str): The word that triggered the error.
            parent_command (str): The primary command in conflict.
            child_command (list of str): Any child commands that were being processed.
        """
        print(ERROR("\nYou cannot request 2 main menu actions at once"))
        print(ERROR(f"The call to '{word}' will be ignored"))
        print(ERROR(f"If you want to execute '{word}', 'cancel' the current job and start over again with '{word}'"))
        print(ERROR(f"Only the menu call to '{parent_command} {child_command}' will be executed:"))


    def multi_menu_call(self, silent=False):
        """
        Processes the user input to validate and execute commands based on pre-defined criteria.
        This method integrates several parsing functions to comprehensively handle the input,
        check for command validity, and optionally execute the command if it is valid.

        The method primarily handles splitting user input into component parts, removing any 
        specified help options, extracting commands, and finalizing command structures. It
        also handles the conditional execution of these commands based on the 'silent' parameter.

        Args:
            silent (bool): If set to True, suppresses the execution feedback, only performing
                        validation without executing the command. This is useful for scenarios
                        where only validation is required without the side effects of command execution.

        Returns:
            bool: True if the command is valid and was executed (or validated in silent mode),
                False if the command is invalid. This allows calling functions to understand the
                outcome of command processing and react accordingly.

        Detailed Steps:
        - Splits the user input into words.
        - Removes recognized help-related options.
        - Attempts to extract a command that might be prefixed with './' indicating a direct command.
        - If no direct command is found, it tries to finalize the commands based on remaining inputs.
        - Checks if the derived parent command is a recognized main menu command.
        - If not silent, and the command is valid, processes the command using the MainMenu class.
        - If silent, simply returns True for a valid command without processing it.
        - Returns False if no valid command is found, indicating an invalid input.
        """
        # Split the input into individual words for processing
        words = str(self.input).split()
        child_command = []

        # Remove help options and determine if a help command was indicated
        parent_command, child_command = self.remove_help_options(words)

        # Process commands based on the presence or absence of a direct command
        if not parent_command:
            # Try to extract a command directly if prefixed with './'
            extracted_command, extracted_child = self.extract_command(child_command)
            if extracted_command:
                parent_command = extracted_command
                child_command = extracted_child
            else:
                # Finalize commands if no direct command was found
                parent_command, child_command = self.finalize_commands(words, parent_command)
        else:
            # If a help command was found, process remaining words to see if a command follows
            extracted_command, _ = self.extract_command(child_command)
            if extracted_command:
                child_command = extracted_command
            else:
                # Finalize commands if no further command extraction is possible
                _, child_command = self.finalize_commands(child_command, parent_command)

        # Validate if the determined parent command is a recognized main menu command
        if parent_command in main_menu:
            if not silent:
                # If not silent, ensure the child_command is in list form for processing
                if not isinstance(child_command, list):
                    child_command = [child_command]
                # Create an instance of MainMenu to process the command
                menu = MainMenu()
                return menu.process_command(parent_command, child_command, context=self.context)
            return True
        else:
            # Print an error message and return False if the command is not recognized
            print(ERROR("\nInvalid menu call, none of the inputs validate as menu"))
            return False 


class DataFormatValidation: 
    
    """
    Placeholder
    """
    print("placeholder")

      
def format_slash_separated_details(format):
    """
    Split the string into parts based on '/'
    """
    parts = format.split('/')

    if len(parts) > 1:
        formatted_string = ', '.join(parts[:-1]) + ' or ' + parts[-1] + '.\n'
        formatted_regex = "^(" + "|".join(parts) + ")$"
    else:
        formatted_string = parts[0] + '.\n'
        formatted_regex = "^(" + parts[0] + ")$'"

    return {'message': f"{formatted_string}",
            'regex': f"{formatted_regex}",
            'decimals': None,
            'percentage': False,
            'auto_validate': True}


def format_number_details(format):
    """
    Split the string into parts based on #.## formating received. 
    Decimal % is also processed.
    """
    percentage = False

    if not all(c in '#.%' for c in format):
        return
    
    if format.endswith("%"):
        format=format[:-1]
        percentage = True

    decimal_point_index = format.find('.')
        
    if decimal_point_index != -1:
        decimal_count = len(format) - decimal_point_index - 1
    else:
        decimal_count = 0

    if decimal_count == 0:
        formatted_string = 'only whole numbers. ex.: 50, 28 , 173...\nAny decimals will be rounded.\n'
        formatted_regex = "^\d+$"
    else:
        formatted_string = f"numbers with up to {decimal_count} decimal places are accepted.\n"
        formatted_regex = r"^\d+(\.\d{1," + str(decimal_count) + "})?$"

    if percentage:
        formatted_string += "Enter as a decimal or percentage (e.g., 0.10 or 10%).\n"
        formatted_regex = r"^\d+(?:\.\d{1," + str(decimal_count) + "})?(?:%?)$"

    return {'message': f"{formatted_string}",
            'regex': f"{formatted_regex}",
            'decimals': f"{decimal_count}",
            'percentage': f"{percentage}",
            'auto_validate': False}


def format_category_check(format):
    if not format_number_details(format):
        format_details = format_slash_separated_details(format)
    else:
        format_details = format_number_details(format)
    return format_details


def format_validation(prompt,format, silent=False):
    """
    Checks input data for formatting issues
    """
    if prompt is None:
        return None if silent else print("Invalid input: None provided")
    
    try:
        format_details = format_category_check(format)
        normalized_input = prompt.replace(',', '.')
           
        if normalized_input.startswith('.'):
            normalized_input = '0' + normalized_input

        if format_details['decimals'] != None:
            if format_details['percentage']:
                if normalized_input.endswith("%"):
                    normalized_input= normalized_input[:-1]
                    number = float(normalized_input)
                    number = number / 100
                else:
                    number = float(normalized_input)
            else:
                number = float(normalized_input)
            normalized_input = f"{number:.{format_details['decimals']}f}"

        if re.match(format_details['regex'], normalized_input):
            return normalized_input
        else:
            raise ValueError(f"Please enter a value in the format: {format_details['message']}")
                    
    except ValueError as e:
        if not silent:
            print(ERROR(f"\nInvalid format detected: {prompt}"))
            print(ERROR(e))
        return None
    

def auto_validator(data):
    """
    Auto-validate data against formatting, fixing possible syntax errors on user entry
    """
    auto_validate_formats = []
    validated_values = []
    invalidated_values = []

    for key, (format, actual_value) in data.items():
        if format_category_check(format)["auto_validate"]:
            auto_validate_formats.append((key, format))
            
    all_values = [(key, actual_value) for key, (_, actual_value) in data.items()]
    
    for key, actual_value in all_values:
        is_validated = False
        for fmt_key, format in auto_validate_formats:
            validated_value = format_validation(actual_value, format, True)
            if validated_value:
                validated_values.append(f"{fmt_key}:{validated_value}")
                is_validated = True
                break 

        if not is_validated and actual_value not in invalidated_values:
            invalidated_values.append(actual_value)

    trade_details = reconstruct_trade_details(validated_values,invalidated_values,data)
    for key, (format, actual_value) in trade_details.items():
        trade_details[key]=(format,format_validation(actual_value, format,True))

    return trade_details


def reconstruct_trade_details(validated, invalidated, original_data):
    trade_details = {}
    
    for key, (fmt, _) in original_data.items():
        trade_details[key] = (fmt, None)
    
    for item in validated:
        if ':' in item:
            key, value = item.split(':')
            if key in trade_details:
                trade_details[key] = (trade_details[key][0], value)
    
    for value in invalidated:
        if value and ':' in value:
            key, val = value.split(':')
            if key in trade_details and trade_details[key][1] is None:
                trade_details[key] = (trade_details[key][0], val)
    
    for value in invalidated:
        if value and ':' not in value: 
            for key, (fmt, val) in trade_details.items():
                if val is None and format_validation(value, fmt,True):
                    trade_details[key] = (fmt, value)
                    break

    return trade_details
# Validations end


# Menu start  
class MainMenu:
    """
    Manages the main menu and command processing for the command line application. This class provides
    a central point for routing and handling commands input by the user, ensuring that each command
    is executed by the appropriate method.

    Attributes:
        command (dict): A dictionary mapping command strings to their respective handler methods.
    """
    def __init__(self):
        """
        Initializes the MainMenu class with a dictionary that associates command names with their
        corresponding methods for handling those commands.
        """
        self.command = {
            "exit": self.exit_program,
            "check": self.menu_check,
            "help": self.menu_help,
            "entry": log_trade,
            "set": self.menu_set,
            "cancel": self.navigate_away,
            "back": self.navigate_away
        }


    def process_command(self,cmd,child_command=None,context=None):
        """
        Processes a given command by looking up the corresponding function and executing it. Handles
        different command behaviors, including those that require additional context or arguments.

        Args:
            cmd (str): The command string as entered by the user.
            child_command (tuple, optional): Additional arguments that might be needed by the command.
            context (str, optional): Contextual information or state that might affect how the command
                                     is executed.

        Returns:
            bool: Returns True if the command was processed successfully, False if the command
                  could not be found or if the execution failed due to context issues.

        This method delegates command execution based on the command dictionary defined in the class.
        It also handles conditional command processing, such as whether additional arguments are present
        or if specific context conditions are met, ensuring that commands like 'entry' and 'set' can
        operate with the necessary parameters.
        """
        function = self.command.get(cmd)

        if function:
            if cmd in ["exit", "check"]:
                return function()
            elif cmd =='help':
                if child_command:
                    return function(*child_command)
                else:
                    return function(context) if context else function()
            elif not context:
                if cmd in ["entry", "set"]:
                    return function(*child_command) if child_command else function()
                elif cmd == "cancel":
                    print(italic(red("\nThere is nothing to cancel at the moment.")))
                elif cmd == "back":
                    print(italic(red("\nThere is nowhere to go back to, you are in home page.")))
            elif context:
                if self.navigate_away():
                    print(SUCCESS("\nLet's continue with a new command!"))
                    if cmd in ["entry","set"]:
                        return function(*child_command) if child_command else function()
                    else:
                        return True
        else:
            return False


    def menu_entry(self,input):
        print("placeholder")


    def menu_set(self):
        """
        Logic for managing settings
        """
        # This going to be a class, just adding place holder
        print("Settings updated successfully.")
        
        
    def menu_check(self):
        """
        Check all trades active and curent stats of the trading strategy
        """
        print("Current Trading Stats:")


    def exit_program(self):
        """
        Executes the process to safely exit the program, ensuring that the user is made aware of any
        unsaved data that could be lost upon exiting.

        This method prompts the user for confirmation before closing the application. It is designed
        to prevent accidental closure of the program, thus safeguarding against the potential loss
        of unsaved progress or important data. The confirmation request informs the user of the risks
        and obtains their explicit consent to proceed with exiting the application.

        If the user confirms their intention to exit, the program will display a farewell message and
        then terminate. If the user decides not to exit, the method will simply return, allowing the
        user to continue their session.

        The process involves:
        1. Informing the user that all non-saved data will be lost.
        2. Asking for user confirmation to proceed with exiting.
        3. Exiting the program if confirmation is received.
        
        Returns:
            None: This method does not return a value but terminates the program if confirmed.
        """
        # print("\n")
        print(ERROR("\nAll non-saved data will be lost"))
        leave = get_input(italic(red("Would you like to quit the program anyways? (y/n)\n")))
        confirmation = yes_or_no(leave)
        
        if confirmation is True:
            print("\nClosing...")
            print(GREETING("See you next time!"))
            exit()


    def navigate_away(self):
        """
        Requests confirmation from the user before navigating away from a current task or job.
        This method is invoked typically when an operation that might have unsaved changes or
        important state is about to be interrupted or cancelled. It ensures that the user is
        aware of the potential loss of progress and confirms their intention to proceed.

        Returns:
            bool: True if the user confirms the navigation away, indicating a willingness to
                  potentially lose unsaved changes or interrupt ongoing tasks. False if the
                  user decides not to proceed, thus maintaining the current state.

        The method uses a prompt to ask the user if they want to proceed with navigation, which
        could cancel the current job. The confirmation is handled by the 'yes_or_no' function,
        which parses user input and returns a boolean value based on the user's response.
        """
        cancel = get_input(italic(red("\nNavigating away will cancel the current job. Do you want to proceed? (y/n):\n")))
        return yes_or_no(cancel)


    def menu_help(self,context=None):
        """
        Displays the help menu with guidance on available commands and additional context-specific help
        if a particular context is provided. This method provides dynamic help content based on user interaction.

        Args:
            context (str, optional): Specifies a particular context for which help is requested. If 'help' is
                                     directly passed as the context, it resets to None to show the main help menu.
                                     Defaults to None, which shows the general help menu.

        Returns:
            bool: False to indicate that the help display loop has ended (typically when user exits help).
        
        The method enters a loop that continues to provide help information until the user decides to exit
        by entering 'back' or 'cancel'. If additional commands are entered, it validates them and potentially
        re-invokes the help with a new context or performs the requested action.
        """
        if context == "help":
            context=None
        
        while True:
            if context is None:
                print(TITLE("Help Information:"))
                print("  - Type 'entry' to enter a trade")
                print("  - Type 'check' to view stats")
                print("  - Type 'set' to open settings")
                print("  - Type 'help' to get help")
                print("  - Type 'back' to return to previous location")
                print("  - Type 'cancel' to cancel current job")
                print("  - Type 'exit' to quit the program")
                print("\nCommands described above can be ran from anywhere in the program.")
                return False
            
            else:
                print(TITLE(f"Help for '{context}':"))
                #context specifics placeholder
                print(" - Type 'back' or 'cancel' to return to where you were")
                print(" - Type 'help' again to see general help")
                print(PATH(f"\n./help {context}"))
                cmd=get_input("Enter command: \n")
                input_validate= InputValidation(cmd,context="help")
                
                if cmd == 'back' or cmd == 'cancel':
                    return False
                elif input_validate.multi_menu_call(silent=True):
                    input_validate.multi_menu_call(cmd)
                else:
                    continue     
        
              
def log_trade(action=None, type=None, price=None, stop=None, atr=None):
    """
    Log a trade with optional user interaction for details.
    """
    print(TITLE("Starting to log a trade..."))
    stop_process=False
    bulk = False
    validation_need = True
    key_none = []
    cmd="entry"
    
    trade_details = {
        "action": ("open/close/update/bulk", action),
        "type": ("long/short", type),
        "price": ("#.########", price),
        "stop": ("#.########", stop),
        "atr": ("#.####%", atr)
    }

    def key_validator(trade_details):
        trade_details = auto_validator(trade_details)
        
        for key,(fmt,value) in trade_details.items():        
            if value is not None:
                trade_details[key]= (fmt,f"{key}:{value}") 
            else:
                key_none.append(key)

        return key_none, trade_details
            
    while True:
        key_none=[]
        
        if any(detail[1] == "bulk" for detail in trade_details.values()):
            bulk = True
            break 

        if validation_need:
            key_none, trade_details = key_validator(trade_details)
            
            while key_none:
                key = key_none[0]
                fmt, _ = trade_details[key]

                print(PATH(f"\n./entry {' '.join(delete_none_values(trade_details,1))}"))
                prompt = get_input(f"Enter trade {key} ({fmt}) or 'help': \n")
                words = prompt.split()

                if "bulk" in words:
                    bulk = True
                    break

                input_validate = InputValidation(prompt, context=cmd)
                if not input_validate.multi_menu_call(silent=True):
                    if len(words) > len(key_none):
                        print(ERROR("\nToo many arguments input, any extra arguments will be ignored."))
                        words = words[:len(key_none)]
                    for word,key in zip(words,key_none):
                        fmt = trade_details[key][0]
                        trade_details[key] = (fmt,word)
                    key_none=[]
                    words=[]
                else:
                    if not input_validate.multi_menu_call():
                        stop_process=False
                    else:
                        stop_process=True 
                        validation_need = False
                        break 

            if not stop_process:
                key_none, trade_details = key_validator(trade_details)

                if not key_none:
                    validation_need = False 
            else:
                break   
        else:
            break
        
    if bulk:
        print("Hey, you selected bulk-mode import!")
    else:
        action, type, price, stop, atr = (trade_details[k][1] for k in trade_details)
        print(SUCCESS(f"\nTrade logged with user input:\nentry {action} {type} {price} {stop} {atr}"))
   
    
def main_loop():
    """
    Executes the main loop of the application, continuously prompting the user for input
    and processing commands until the program is exited. This loop is the primary interaction
    point for users, providing a command line interface to access various functionalities
    of the system.

    The main loop performs several key functions:
    - It welcomes the user and introduces them to the system.
    - Displays the main help menu to assist the user in understanding available commands.
    - Provides professional tips for using the system more effectively.
    - Continuously requests and processes user commands, utilizing the MainMenu and InputValidation
      classes to handle command execution and validation.

    This loop runs indefinitely, processing input commands until an exit command is issued
    by the user or the program is terminated through other means.
    """
    print(underscore(GREETING("\n\n\nWelcome to Trading Book System!")))
    menu = MainMenu()
    menu.menu_help()
    pro_tips()
    
    while True:
        print(PATH("\n./"))
        cmd = get_input("Enter a valid command or 'help': \n")
        if cmd:
            input_validate=InputValidation(cmd)
            input_validate.multi_menu_call()

        
if __name__ == "__main__":
    main_loop()
