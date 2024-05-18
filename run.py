import re
import gspread
from gspread.exceptions import APIError
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError, DefaultCredentialsError


# Define the Google API scopes that the application will need access to.


class DataBaseActions:
    """
    This class provides methods to interact with a Google Sheets spreadsheet. It allows reading data
    from and writing data to specific worksheets within the spreadsheet.

    Attributes:
        SCOPE (list): A list of scopes required for accessing Google Sheets and Google Drive.
        CREDS (Credentials): Credentials object created from the service account file.
        SCOPED_CREDS (Credentials): Credentials object with specified scopes.
        GSPREAD_CLIENT (gspread.Client): Authorized gspread client.
        SHEET (gspread.Spreadsheet): The Google Sheets spreadsheet object.
    """

    def __init__(self):
        """
        Initializes the DataBaseActions class by setting up the necessary Google API credentials
        and authorizing the gspread client to access the specified spreadsheet.
        """
        try:
            self.SCOPE = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive",
            ]
            self.CREDS = Credentials.from_service_account_file("creds.json")
            self.SCOPED_CREDS = self.CREDS.with_scopes(self.SCOPE)
            self.GSPREAD_CLIENT = gspread.authorize(self.SCOPED_CREDS)
            self.SHEET = self.GSPREAD_CLIENT.open("trading_book")
        except DefaultCredentialsError as e:
            print(f"Failed to load credentials from service account file: {e}")
        except GoogleAuthError as e:
            print(f"Failed to authenticate with Google API: {e}")
        except APIError as e:
            print(f"Failed to authorize gspread client: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during initialization: {e}")

    def read(self, worksheet):
        """
        Reads the last row of data from the specified worksheet.

        Args:
            worksheet (str): The name of the worksheet to read from.

        Returns:
            list: The last row of data from the worksheet.
        """
        try:
            worksheet = self.SHEET.worksheet(worksheet)
            data = worksheet.get_all_values()
            data_row = data[-1]

            return data_row
        except APIError as e:
            print(f"Failed to read from worksheet {worksheet}: {e}")
        except Exception as e:
            print(
                f"An unexpected error occurred while reading the worksheet {worksheet}: {e}"
            )

    def write(self, worksheet, data):
        """
        Appends a new row of data to the specified worksheet.

        Args:
            worksheet (str): The name of the worksheet to write to.
            data (list): The data to append as a new row in the worksheet.
        """
        try:
            worksheet = self.SHEET.worksheet(worksheet)
            worksheet.append_row(data)
        except APIError as e:
            print(f"Failed to write to worksheet {worksheet}: {e}")
        except Exception as e:
            print(
                f"An unexpected error occurred while writing to the worksheet {worksheet}: {e}"
            )


##Styling


class StyleOutput:
    """
    Provides methods to print messages with various ANSI escape code based styles. This class simplifies the
    process of applying text styles such as colors, bold, and underline in console outputs.

    Attributes:
        styles (dict): A dictionary mapping style names to their corresponding ANSI escape codes.
    """

    _styles = {
        "red": "\033[31m",
        "green": "\033[32m",
        "cyan": "\033[96m",
        "gray": "\033[2m",
        "orange": "\033[1m\033[38;5;208m",
        "bold": "\033[1m",
        "italic": "\033[3m",
        "dim": "\033[2m",
        "underscore": "\033[4m",
        "none": "\033[0m",
        "title": "\n\n\n\033[1m\033[32m   ",
        "green_background": "\033[1m\033[42m\033[97m",
        "error": "\033[1m\033[41m\033[97m",
    }

    @classmethod
    def apply_style(cls, style_name):
        """
        Applies the specified style to a message.

        Args:
            style_name (str): The name of the style to apply. Must be a key in the `styles` dictionary.

        Returns:
            function: A function that takes a message as an argument and returns the styled message.
        """

        def styled_message(message):
            return f"{cls._styles[style_name]}{message}{cls._styles['none']}"

        return styled_message

    @staticmethod
    def path_style(cmd=None, args=None):
        if cmd is None:
            return gray(f"\n./")
        elif args is None:
            return gray(f"\n./{cmd}")
        else:
            return gray(f"\n./{cmd} {' '.join(delete_none_values(args,1))}")


##Styling atributes

styles = StyleOutput()
gray = styles.apply_style("gray")
red = styles.apply_style("red")
green = styles.apply_style("green")
bold = styles.apply_style("bold")
italic = styles.apply_style("italic")
underscore = styles.apply_style("underscore")
dim = styles.apply_style("dim")
GREETING = styles.apply_style("orange")
TITLE = styles.apply_style("title")
QUESTION = styles.apply_style("cyan")
SUCCESS = styles.apply_style("green_background")
ERROR = styles.apply_style("error")
DB = DataBaseActions()


##General usage functions


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
    input_data = str(user_input.strip().lower()).split()

    # Return the input after stripping whitespace and converting to lowercase

    return input_data


def delete_none_values(data_details, num):
    """
    Filters out None values from a specified field in a dictionary of details.

    This function is useful for cleaning data by removing None entries from a collection
    of information before further processing or display. It ensures that only
    valid, non-None data is kept for subsequent operations.

    Args:
        data_details (dict): A dictionary where each key is an identifier and each value
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

    trade_values = [value[num] for value in data_details.values()]

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

    affirmative = [
        "y",
        "yes",
        "yeap",
        "yeah",
        "ya",
        "ye",
        "yy",
        "yees",
        "yess",
        "sure",
        "absolutely",
        "indeed",
    ]
    negative = ["n", "no", "nope", "nah", "not", "dont", "nn", "nno", "noo", "never"]

    while True:
        if isinstance(input, list) and len(input) > 0:
            input = input[0]
        if input in affirmative:
            confirm = True
            break
        elif input in negative:
            confirm = False
            break
        else:
            # Inform the user of invalid input and request a valid response

            print(ERROR("\nPlease use 'y' or 'n'."))
            input = get_input("\nEnter new response:\n")
            continue
    return confirm


def PATH(cmd=None, data_settings=None, key=None):
    """
    Prints the path style based on the provided command and data settings, and prompts the user
    for input depending on the format specified in the data settings.

    Args:
        cmd (str, optional): The command string to be styled and printed.
        data_settings (dict, optional): A dictionary containing settings that determine the
                                        format of the user prompt.
        key (str, optional): The key to look up in the data_settings to determine the format
                             of the user prompt.

    Returns:
        str: The user input based on the specified format in the data_settings.

    The function performs the following steps:
    1. Prints the styled command path.
    2. Prompts the user for input based on the data_settings and key:
       - If data_settings is None, it prompts the user to enter a command.
       - If data_settings is provided, it looks up the format (fmt) for the specified key.
         - If fmt is "any", it prompts the user to enter any characters except spaces or menu calls.
         - If the input does not contain ":", it prepends the key to the input.
         - For other formats, it prompts the user to enter input based on the specified format.
    """
    # Print the styled command path

    print(styles.path_style(cmd, data_settings))

    # Check if data_settings is provided

    if data_settings is None:
        # Prompt the user to enter a command

        prompt = get_input("Enter command: \n")
    else:
        # Look up the format for the specified key in the data_settings

        fmt, _ = data_settings[key]

        # Check if the format is "any"

        if fmt == "any":
            # Prompt the user to enter any characters except spaces or menu calls

            prompt = get_input(
                f"Enter trade {key} (any characteres, but space or menu calls) or 'help': \n"
            )

            # If the input does not contain ":", prepend the key to the input

            is_menu = InputValidation(prompt).multi_menu_call(silent=True)

            if not is_menu:
                if ":" not in prompt:
                    # Prompt the user to enter input based on the specified format

                    prompt[0] = f"{key}:{prompt[0]}"
        else:
            prompt = get_input(f"Enter trade {key} ({fmt}) or 'help': \n")
    return prompt


## Validations


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

    def __init__(self, input, context=None):
        """
        Initializes the InputValidation instance with user input and optional context.

        Args:
            input (str): Raw user input string.
            context (str, optional): Contextual information relevant to input processing.
        """
        self.input = input
        self.context = context

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

        help_options = {"help", "./help"}

        # Filter out the help keywords from the list of words

        no_help_words = []

        # Check if any help keywords were in the original words list

        no_help_words[:] = [word for word in words if word not in help_options]

        # Return both whether help was detected and the cleaned list of words

        return (
            "help" if any(option in words for option in help_options) else ""
        ), no_help_words

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
        return "", words

    def finalize_commands(self, words, parent_command):
        """
        Finalizes the identification of the parent command and constructs the list of child commands
        based on the remaining words in the input. This method consolidates the parsing process by
        establishing a clear hierarchical command structure after initial command identification has been done.

        This method is crucial in the command processing pipeline, as it determines the ultimate command
        that should be executed based on user input, along with any sub-commands or parameters that need
        to be passed to the command handler functions.

        Args:
            words (list of str): A list of words that remains after initial filtering for direct commands
                                and help-related options. These words are potential commands or parameters.
            parent_command (str): The command that has been initially identified as the primary action
                                the user wants to perform. This could still be None if no clear command
                                was identified in earlier stages.

        Returns:
            tuple: A tuple containing:
                - parent_command (str): The finalized parent command if one is identified among the words.
                                        If no new command is found and a parent_command was already identified,
                                        it remains unchanged.
                - child_command (list of str): A list of additional commands or parameters that accompany the
                                            parent command. This list is used to further execute the command.

        Process:
            - The method iterates over the list of remaining words.
            - If a word matches one of the predefined commands and no parent command has been set, it establishes
            this word as the parent command.
            - If a parent command is already set and it is 'help', it looks to set the next valid command as a
            child command intended to provide specific help.
            - If a word doesn't match any predefined command or is additional to an existing command, it is added
            to the list of child commands as a parameter or sub-command.
            - If there are any conflicts or issues (like a word trying to act as a second parent command), it logs
            an error specific to this scenario.

        Example:
            - Input: ['entry', 'open'], parent_command: None
            Output: ('entry', ['open'])
            - This means the parent command is 'entry' with 'open' as a sub-command or parameter.
        """
        child_command = []
        cancelled_commands = []

        for word in words:
            if word.startswith("./"):
                word = word[2:]
            if word in main_menu:
                if not parent_command:
                    # Set the word as parent command if no parent command has been identified yet

                    parent_command = word
                elif parent_command == "help" and not child_command:
                    # If the parent command is 'help' and no child command has been set, set this word as child command

                    child_command = word
                else:
                    cancelled_commands.append(word)
            else:
                # Append non-command words as child commands or parameters

                child_command.append(word)
        if cancelled_commands:
            # Handle errors when an invalid command structure is detected

            self.print_command_error(cancelled_commands, parent_command, child_command)
        return parent_command, child_command

    def print_command_error(self, words, parent_command, child_command):
        """
        Displays error messages for command conflicts, typically when multiple main commands
        are requested simultaneously.

        Args:
            word (str): The word that triggered the error.
            parent_command (str): The primary command in conflict.
            child_command (list of str): Any child commands that were being processed.
        """
        print(ERROR("\nYou cannot request more than one main menu actions at once"))
        print(ERROR(f"The call to '{words}' will be ignored"))
        print(
            ERROR(
                f"If you want to execute '{words}', 'cancel' the current job and start over again with one of the commands in '{words}'"
            )
        )
        print(
            ERROR(
                f"Only the menu call to '{parent_command} {child_command}' will be executed:"
            )
        )

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

        words = self.input
        child_command = []

        # Remove help options and determine if a help command was indicated

        parent_command, child_command = self.remove_help_options(words)

        # Process commands based on the presence or absence of a direct command

        if not parent_command:
            # Try to extract a command directly if prefixed with './'

            extracted_command, extracted_child = self.extract_command(child_command)
            if extracted_command:
                parent_command = extracted_command
                _, child_command = self.finalize_commands(
                    extracted_child, parent_command
                )
            else:
                # Finalize commands if no direct command was found

                parent_command, child_command = self.finalize_commands(
                    words, parent_command
                )
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
                return menu.process_command(
                    parent_command, child_command, context=self.context
                )
            return True
        else:
            # Print an error message and return False if the command is not recognized

            if not silent:
                print(ERROR("\nInvalid menu call, none of the inputs validate as menu"))
            return False


class DataFormatValidation:
    """
    A class to validate and process input data based on predefined formats.
    """

    def __init__(self, input_dictionary, input_data):
        """
        Initialize the DataFormatValidation class.

        Parameters:
        - input_dictionary (dict): Dictionary with the expected formats for each key.
        - input_data (list): List of input data strings to be validated and processed.
        """
        self.input_dictionary = input_dictionary
        self.input_data = input_data
        self.invalidated_data = []
        self.output_dictionary = {
            key: (fmt, None) for key, (fmt, _) in input_dictionary.items()
        }

    def has_colon(self, input):
        """
        Check if the input string contains a colon and split it into key-value pair.

        Parameters:
        - input (str): Input string to check.

        Returns:
        - tuple: (key, value) if colon is present, otherwise (None, input).
        """
        if ":" in input:
            key, value = input.split(":", 1)
            return key, value
        else:
            return None, input

    def format_slash_separated_details(self, format):
        """
        Processes a format string separated by slashes ('/') to create a human-readable format
        string and a corresponding regular expression for input validation. This function is typically
        used to define and validate user inputs based on multiple acceptable formats or options.

        Args:
            format (str): A string that contains various format options separated by slashes.
                        For example, "open/close/update".

        Returns:
            dict: A dictionary containing:
                - 'message': A string that describes the acceptable formats in a readable manner.
                - 'regex': A regular expression string that matches any of the options specified in the format string.
                - 'decimals': None, indicating no specific decimal format is enforced here.
                - 'percentage': False, indicating these format options do not pertain to percentages.
                - 'auto_validate': True, suggesting that inputs matching this format can be automatically validated.

        Example:
            format = "open/close/update"
            Returns -> {
                'message': "open, close, or update.\n",
                'regex': "^(open|close|update)$",
                'decimals': None,
                'percentage': False,
                'auto_validate': True
            }

        The function is ideal for parsing and validating commands or options where multiple choices are allowed.
        """

        # Split the format string by slashes to separate out the different options

        parts = format.split("/")

        # If there are multiple parts, format them into a readable string and regex pattern

        if len(parts) > 1:
            # Creates a formatted string for the message, using commas and 'or' before the last item

            formatted_string = ", ".join(parts[:-1]) + " or " + parts[-1] + ".\n"
            # Creates a regex pattern that matches any of the options (this is wrapped in ^ and $ to match whole strings only)

            formatted_regex = "^(" + "|".join(parts) + ")$"
        else:
            # If there's only one part, format it simply without additional punctuation or conjunctions

            formatted_string = parts[0] + ".\n"
            # Regex for a single option should simply match that exact string

            formatted_regex = "^(" + parts[0] + ")$'"
        # Return a dictionary containing the formatted message, regex, and other relevant details

        return {
            "message": f"{formatted_string}",
            "regex": f"{formatted_regex}",
            "decimals": None,
            "percentage": False,
            "auto_validate": True,
        }

    def format_number_details(self, format):
        """
        Analyzes and constructs a formatting guideline and regular expression based on a numerical
        format string. This function is tailored to handle formats involving decimal numbers and can
        also process percentage values indicated by a trailing '%'.

        Args:
            format (str): A format string specifying the numerical format, potentially including
                        a decimal point and a percent symbol. Examples: '#.##', '#.##%', '###'.

        Returns:
            dict: A dictionary containing:
                - 'message': A user-friendly message describing the acceptable number format.
                - 'regex': A regular expression designed to validate user inputs against the specified format.
                - 'decimals': The number of decimal places expected, based on the format string.
                - 'percentage': A boolean indicating whether the format includes percentage values.
                - 'auto_validate': A flag indicating whether the format should be automatically validated; set to False here.

        Example:
            format = '#.##%'
            Returns -> {
                'message': "numbers with up to 2 decimal places are accepted.\nEnter as a decimal or percentage (e.g., 0.10 or 10%).\n",
                'regex': r'^\d+(?:\.\d{1,2})?(?:%?)$',
                'decimals': 2,
                'percentage': True,
                'auto_validate': False
            }

        The function first checks if the format includes only numbers, decimals, or percent signs.
        If the format ends with a percent sign, it notes that percentages are expected and adjusts the format.
        It then determines the number of decimals by finding the position of the decimal point.
        """
        # Initial setting for whether the format involves percentages

        percentage = False

        # Validate that the format contains only number-related characters

        if not all(c in "#.%" for c in format):
            return
        # Adjust for percentage formats by stripping the '%' sign and setting the flag

        if format.endswith("%"):
            format = format[:-1]
            percentage = True
        # Determine the position of the decimal point to calculate decimal precision

        decimal_point_index = format.find(".")

        # Calculate the number of decimal places based on the position of the decimal point

        if decimal_point_index != -1:
            decimal_count = len(format) - decimal_point_index - 1
        else:
            decimal_count = 0
        # Construct the appropriate message and regex based on the number of decimals

        if decimal_count == 0:
            formatted_string = "only whole numbers. ex.: 50, 28 , 173...\nAny decimals will be rounded.\n"
            formatted_regex = "^\d+$"
        else:
            formatted_string = (
                f"numbers with up to {decimal_count} decimal places are accepted.\n"
            )
            formatted_regex = r"^\d+(\.\d{1," + str(decimal_count) + "})?$"
        # Append percentage handling to the message and regex if applicable

        if percentage:
            formatted_string += (
                "Enter as a decimal or percentage (e.g., 0.10 or 10%).\n"
            )
            formatted_regex = r"^\d+(?:\.\d{1," + str(decimal_count) + "})?(?:%?)$"
        # Return a dictionary containing the format details and validation tools

        return {
            "message": f"{formatted_string}",
            "regex": f"{formatted_regex}",
            "decimals": f"{decimal_count}",
            "percentage": f"{percentage}",
            "auto_validate": False,
        }

    def format_category_check(self, format):
        """
        Determines the appropriate formatting details for a given format string by checking if the
        format should be handled as a numerical or slash-separated list. This function acts as a
        dispatcher, invoking the correct formatting function based on the characteristics of the
        format string.

        Args:
            format (str): A format string that may represent numerical values or a list of options
                        separated by slashes. Examples include '#.##', 'open/close/update'.

        Returns:
            dict: A dictionary containing formatting details such as the message for users, regex patterns
                for validation, and flags indicating the type of validation needed (e.g., decimals, percentages).

        Process:
            - The function first attempts to process the format as a numerical detail using `format_number_details`.
            - If `format_number_details` returns `None`, which indicates the format does not fit the expected
            numerical pattern, it then attempts to process the format using `format_slash_separated_details`.
            - This approach allows the function to flexibly handle a variety of input format specifications, adapting
            the processing method based on the format content.

        Example Usage:
            - For a numerical format: '##.##'
            The function will use `format_number_details` to generate appropriate format details.
            - For a command format: 'start/stop/reset'
            The function will use `format_slash_separated_details` to generate format details.

        Note:
            - This function requires that the format string be appropriately prepared to match one of the known
            pattern types (numerical or slash-separated). If neither pattern matches, the return will be the result
            of attempting a numerical format parsing by default.
        """
        # If 'any' Return a dictionary containing the formatted message, regex, and other relevant details

        if format == "any":
            return {
                "message": "any string is accepted.\n",
                "regex": ".*",
                "decimals": None,
                "percentage": False,
                "auto_validate": True,
            }
        else:
            # Attempt to process the format as a numerical detail first

            format_details = self.format_number_details(format)

            # If the format is not numerical, process it as a slash-separated list

            if format_details is None:
                format_details = self.format_slash_separated_details(format)
        # Return the determined format details

        return format_details

    def format_validation(self, prompt, format, silent=False):
        """
        Validates a user's input against a specified format to ensure it conforms to expected patterns.
        This function is essential for maintaining data integrity and ensuring user inputs are processed
        correctly throughout the application.

        Args:
            prompt (str): The user input string to validate.
            format (str): The format string that the input should conform to. This can be a numerical format
                        (like '#.##') or a set of allowable strings (like 'yes/no/maybe').
            silent (bool): If True, suppresses error messages; only returns None if validation fails.
                        Useful for checks where no user feedback is needed.

        Returns:
            str: The normalized and validated input if it conforms to the specified format.
            None: If the input does not conform to the format, or if the input is None.

        Raises:
            ValueError: If the input does not match the format and silent is False, providing details
                        on the required format.

        Process:
            - First, checks if the input is None, immediately returning None if true, optionally printing
            an error if not in silent mode.
            - Uses `format_category_check` to determine the necessary validation details based on the provided format.
            - Normalizes the input by replacing commas with dots to handle decimal inputs correctly.
            - Adjusts the input for percentage values if required by the format.
            - Validates the input against a compiled regular expression derived from the format.
            - If validation fails and silent is False, raises a ValueError with a descriptive message.

        Example Usage:
            - Input validation for a decimal number: format_validation('123.456', '#.##')
            - Input validation for a command choice: format_validation('yes', 'yes/no/maybe')
        """
        # Check for empty value

        if prompt is None:
            return None if silent else print("Invalid input: None provided")
        try:
            # Obtain the validation rules from the format specification

            format_details = self.format_category_check(format)
            normalized_input = prompt.replace(",", ".")

            # Add leading zero to decimal inputs if necessary

            if normalized_input.startswith("."):
                normalized_input = "0" + normalized_input
            # Process numerical inputs for decimal and percentage correctness

            if format_details["decimals"] is not None:
                if format_details["percentage"]:
                    if normalized_input.endswith("%"):
                        normalized_input = normalized_input[:-1]
                        number = float(normalized_input)
                        number = number / 100
                    else:
                        number = float(normalized_input)
                else:
                    number = float(normalized_input)
                normalized_input = f"{number:.{format_details['decimals']}f}"
            # Validate the final input against the expected regex pattern

            if re.match(format_details["regex"], normalized_input):
                return normalized_input
            else:
                raise ValueError(
                    f"Please enter a value in the format: {format_details['message']}"
                )
        except ValueError as e:
            if not silent:
                print(f"\nInvalid format detected: {prompt}")
                print(e)
            return None

    def auto_validator(self, data):
        """
        Automatically validates data entries against defined format rules and attempts to correct
        any syntax errors or format discrepancies in user entries. This function is pivotal in ensuring
        data consistency and correctness before processing or storing user input.

        Args:
            data (dict): A dictionary where each key is an attribute name and each value is a tuple
                        containing a format string and the actual value to validate.

        Returns:
            dict: A dictionary of the same structure as the input, where values are replaced with
                their validated or corrected forms if validation was successful.

        Details:
            - The function first identifies which data entries can be automatically validated based on
            the 'auto_validate' property derived from their format specifications.
            - It processes each data entry, attempting to validate each according to its specified format.
            - Valid entries are corrected and normalized as necessary, while invalid entries are collected
            for potential further review or error handling.
            - Finally, it reconstructs the data details with all validated and corrected values, ensuring
            that each entry conforms to its declared format.

        Process:
            - Initialize lists to track formats that support automatic validation and to separate
            validated from invalidated entries.
            - Iterate over all entries, applying format validation. Successful validations are noted,
            and unsuccessful ones are flagged.
            - Reconstruct the full set of data details with validated entries, using a helper function
            to ensure all entries are either validated or marked for review.

        Example Usage:
            - Given data: {'price': ('#.##', '100.05'), 'type': ('open/close', 'open')}
            The function will confirm '100.05' as a valid decimal and 'open' as a valid option,
            returning the data with the values intact but confirmed as valid.
        """
        auto_validate_formats = []
        validated_values = []
        invalidated_values = []

        # Determine which formats can be automatically validated

        for key, (format, actual_value) in data.items():
            if self.format_category_check(format)["auto_validate"]:
                auto_validate_formats.append((key, format))
        # Prepare to validate all provided values

        all_values = [(key, actual_value) for key, (_, actual_value) in data.items()]

        # Validate each value against its corresponding format

        for key, actual_value in all_values:
            is_validated = False
            for fmt_key, format in auto_validate_formats:
                validated_value = self.format_validation(actual_value, format, True)
                if validated_value:
                    validated_values.append(f"{fmt_key}:{validated_value}")
                    is_validated = True
                    break
            if not is_validated and actual_value not in invalidated_values:
                invalidated_values.append(actual_value)
        # Reconstruct data details with validated values

        data_details = self.reconstruct_data_details(
            validated_values, invalidated_values, data
        )
        for key, (format, actual_value) in data_details.items():
            data_details[key] = (
                format,
                self.format_validation(actual_value, format, True),
            )
        return data_details

    def reconstruct_data_details(self, validated, invalidated, original_data):
        """
        Reconstructs the data details with validated values and attempts to incorporate invalidated values
        where possible. This function is crucial for ensuring that all data is as accurate and complete
        as possible post-validation.

        Args:
            validated (list): A list of validated values in the format 'key:value'.
            invalidated (list): A list of values that failed validation or were not automatically validated.
            original_data (dict): The original dictionary of data with keys and format specifications.

        Returns:
            dict: A dictionary containing the reconstructed data details, with values updated to include
                validated entries and, where possible, invalidated entries that have been corrected.

        Process:
            - Initializes a new dictionary for data details, setting each entry initially to None.
            - Updates this dictionary with validated values, ensuring all keys have their associated correct values.
            - Attempts to assign invalidated values to their corresponding keys if those keys still have None values,
            prioritizing values that fit the original data format.
            - For invalidated values without a colon (indicating they were not split into key:value pairs), attempts
            to validate and assign them to any key that still has a None value.

        Example Usage:
            - Validated: ['price:100.05', 'action:open']
            - Invalidated: ['price:1000', 'stop:']
            - Original Data: {'price': ('#.##', ''), 'type': ('open/close', ''), 'price': ('#', '')}
            The function will construct a dictionary with 'price' set to '100.05', 'type' set to 'open',
            and 'price' set to '1000' if '1000' validates successfully against the '#' format.
        """
        data_details = {key: (fmt, None) for key, (fmt, _) in original_data.items()}

        # Update data details with validated entries

        for item in validated:
            if ":" in item:
                key, value = item.split(":", 1)
                if key in data_details:
                    data_details[key] = (data_details[key][0], value)
        # Attempt to update details with invalidated entries that have specific keys

        for value in invalidated:
            if value and ":" in value:
                key, val = value.split(":", 1)
                if key in data_details and data_details[key][1] is None:
                    data_details[key] = (data_details[key][0], val)
        # Attempt to find a match for invalidated values without specific keys

        for value in invalidated:
            if value and ":" not in value:
                for key, (fmt, val) in data_details.items():
                    if val is None and self.format_validation(value, fmt, True):
                        data_details[key] = (fmt, value)
                        break
        return data_details

    def process_input_data(self):
        """
        Process the input data to validate and categorize them based on the predefined formats.

        This method performs three passes:
        1. Handle key-value pairs.
        2. Handle percentage values.
        3. Handle remaining values for all None values in the dictionary.
        """
        remaining_data = []
        processed_keys = set()  # Track processed keys

        if self.input_data:
            remaining_data = self.handle_key_value_pairs(
                self.input_data, processed_keys
            )
            remaining_data = self.handle_percentage_values(
                remaining_data, processed_keys
            )
            self.handle_remaining_values(remaining_data, processed_keys)

    def handle_key_value_pairs(self, input_data, processed_keys):
        """
        Processes input data to handle key-value pairs.

        This method validates and updates the output dictionary with key-value pairs from the input data,
        ensuring that each key is processed only once. If a key already has a value, it asks for user
        confirmation before overwriting it. Non-key-value inputs and menu calls are collected for further
        processing.

        Args:
            input_data (list): List of input data strings to be processed.
            processed_keys (set): Set of keys that have already been processed to avoid duplicates.

        Returns:
            list: A list of remaining data items that were not processed as key-value pairs.

        """
        remaining_data = []
        for item in input_data:
            key, value = self.has_colon(item)

            if key:
                if key in self.input_dictionary and key not in processed_keys:
                    format = self.input_dictionary[key][0]
                    validated_value = self.format_validation(value, format, True)

                    if validated_value:
                        if self.output_dictionary[key][1] is None:
                            self.output_dictionary[key] = (
                                format,
                                f"{key}:{validated_value}",
                            )
                            processed_keys.add(key)  # Mark key as processed
                        else:
                            if yes_or_no(
                                message=f"{key} already has a value. Do you want to overwrite it?"
                            ):
                                self.output_dictionary[key] = (
                                    format,
                                    f"{key}:{validated_value}",
                                )
                                processed_keys.add(key)  # Mark key as processed
                            else:
                                self.invalidated_data.append(item)
                    else:
                        self.invalidated_data.append(item)
                else:
                    self.invalidated_data.append(item)
            else:
                # Check if the item is a menu call

                is_menu = InputValidation([item]).multi_menu_call(silent=True)
                if not is_menu:
                    remaining_data.append(item)
        return remaining_data

    def handle_percentage_values(self, remaining_data, processed_keys):
        """
        Processes remaining data to handle percentage values.

        This method validates and updates the output dictionary with percentage values from the remaining data,
        ensuring that each key is processed only once. It converts percentage strings to their decimal equivalents
        before validation. Non-percentage inputs are collected for further processing.

        Args:
            remaining_data (list): List of remaining data items to be processed.
            processed_keys (set): Set of keys that have already been processed to avoid duplicates.

        Returns:
            list: A list of remaining data items that were not processed as percentage values.

        """
        percentage_keys = [
            key
            for key, (format, value) in self.output_dictionary.items()
            if format.endswith("%")
        ]
        for item in remaining_data[:]:
            original_item = item  # Store the original item

            if item.endswith("%"):
                for key in percentage_keys:
                    if (
                        self.output_dictionary[key][1] is None
                        and key not in processed_keys
                    ):
                        format = self.input_dictionary[key][0]
                        format_details = self.format_category_check(format)
                        item = item[:-1]  # Remove the percentage sign for validation
                        try:
                            item_as_float = float(item) / 100
                            item = f"{item_as_float:.{format_details['decimals']}f}"
                            validated_value = self.format_validation(item, format, True)

                            if validated_value:
                                self.output_dictionary[key] = (
                                    format,
                                    f"{key}:{validated_value}",
                                )
                                remaining_data.remove(
                                    original_item
                                )  # Remove the original item
                                processed_keys.add(key)  # Mark key as processed
                                break
                        except ValueError:
                            self.invalidated_data.append(original_item)
                            break
        return remaining_data

    def handle_remaining_values(self, remaining_data, processed_keys):
        """
        Processes remaining data to handle non-key-value and non-percentage values.

        This method validates and updates the output dictionary with values from the remaining data,
        ensuring that each key is processed only once. It checks for keys that are still None and updates
        them with the first matching value from the input. Remaining invalid data is collected for reporting.

        Args:
            remaining_data (list): List of remaining data items to be processed.
            processed_keys (set): Set of keys that have already been processed to avoid duplicates.

        """
        for item in remaining_data[:]:
            original_item = item  # Store the original item
            validated = False

            for key, (format, value) in self.input_dictionary.items():
                if key in processed_keys:
                    continue
                if (
                    value is None and not format.endswith("%") and format != "any"
                ):  # Skip percentage and 'any' formats
                    validated_value = self.format_validation(item, format, True)
                    if validated_value:
                        self.output_dictionary[key] = (
                            format,
                            f"{key}:{validated_value}",
                        )
                        remaining_data.remove(original_item)  # Remove the original item
                        processed_keys.add(key)  # Mark key as processed
                        validated = True
                        break
                elif value is not None:
                    # If a value is already set and the format is not key:value, do not update it

                    if ":" not in item:
                        continue
                    validated_value = self.format_validation(item, format, True)

                    if validated_value:
                        self.output_dictionary[key] = (
                            format,
                            f"{key}:{validated_value}",
                        )
                        remaining_data.remove(original_item)
                        processed_keys.add(key)  # Mark key as processed
                        validated = True
                        break
            if not validated:
                self.invalidated_data.append(original_item)

    def print_errors(self):
        """
        Print any invalidated data and remaining input data that were not processed.
        """
        if self.invalidated_data:
            print(ERROR("\nSome data could not be validated as any valid arguments."))
            print(italic(red(dim(f"Ivalidated data: {self.invalidated_data}"))))

    def get_results(self):
        """
        Process the input data and return the results.

        Returns:
        - output_dictionary: Dictionary with validated and processed data.
        - invalidated_data: List of data that could not be validated.
        - input_data: List of remaining input data that were not processed.
        """
        if self.input_data:
            self.process_input_data()
            self.print_errors()
            return self.output_dictionary, self.invalidated_data, self.input_data


## Menu


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
            "entry": self.menu_entry,
            "set": self.menu_set,
            "cancel": self.navigate_away,
            "back": self.navigate_away,
        }

    def process_command(self, cmd, child_command=None, context=None):
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
        # Get the function associated with the command from the command dictionary

        function = self.command.get(cmd)

        if function:
            # Handle simple commands that do not require additional arguments or context

            if cmd in ["exit", "check"]:
                return function()
            # Handle the 'help' command with optional child_command or context

            elif cmd == "help":
                if child_command:
                    return function(child_command)
                else:
                    return function(context) if context else function()
            # Handle commands that do not have a specific context

            elif not context:
                if cmd in ["entry", "set"]:
                    # Explicitly check for empty list and treat it as no additional arguments

                    if child_command == []:
                        return function()
                    else:
                        return function(child_command) if child_command else function()
                elif cmd == "cancel":
                    # Print a message if there is nothing to cancel

                    print(italic(red("\nThere is nothing to cancel at the moment.")))
                elif cmd == "back":
                    # Print a message if there is nowhere to go back to

                    print(
                        italic(
                            red(
                                "\nThere is nowhere to go back to, you are in home page."
                            )
                        )
                    )
            # Handle commands with a specific context

            elif context:
                cancel = self.navigate_away(child_command)
                if cancel:
                    # If navigation away is confirmed, print a success message and process the new command

                    print(SUCCESS("\nLet's continue with a new command!"))
                    if cmd in ["entry", "set"]:
                        return function(child_command) if child_command else function()
                return cancel
        else:
            # Return False if the command is not found in the command dictionary

            return False

    def menu_entry(self, child_command=None):
        """
        Initializes an Entry instance and starts the entry loop.
        """
        entry_instance = Entry(child_command)
        entry_instance.entry_loop()

    def menu_set(self, child_command=None):
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
        print(ERROR("\nAll non-saved data will be lost"))
        leave = get_input(
            italic(red("Would you like to quit the program anyways? (y/n)\n"))
        )
        confirmation = yes_or_no(leave)

        if confirmation is True:
            print("\nClosing...")
            print(GREETING("See you next time!"))
            exit()

    def navigate_away(self, cancel=None):
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
        if not cancel:
            cancel = get_input(
                italic(
                    red(
                        "\nNavigating away will cancel the current job. Do you want to proceed? (y/n):\n"
                    )
                )
            )
        return yes_or_no(cancel)

    def menu_help(self, context=None):
        """
        Calls Help Class and initiate help_loop
        """
        if context == "help":
            context = None
        Help(context=context).help_loop()

    @classmethod
    def get_menu_keys(cls):
        return list(cls().command.keys())


class Entry:
    """
    Class to handle trade entries.
    """

    def __init__(self, input=None):
        """
        Initialize the Entry class.

        Args:
            input (list, optional): Initial input data. Defaults to None.

        This method sets up the initial state of the Entry object, including the input data and
        the data settings required for logging trades. It then starts the entry loop to process
        the trade entry.
        """
        self.input = input
        self.data_settings = {
            "action": ("open/close/update/bulk", None),
            "asset": ("any", None),
            "type": ("long/short", None),
            "price": ("#.########", None),
            "stop": ("#.########", None),
            "atr": ("#.####%", None),
        }
        self.cmd = "entry"

    def key_validator(self):
        """
        Validate the keys in data_settings, checking for None values.

        This method validates the current data settings to identify any keys that have not been provided
        with values. It updates the data settings based on the input data and returns a list of keys that
        still need values.

        Returns:
            tuple: A list of keys with None values and the updated data_settings dictionary.

        Example:
            If 'self.data_settings' contains:
            {
                "action": ("open/close/update/bulk", None),
                "asset": ("any", "AAPL"),
                "type": ("long/short", None),
                "price": ("#.########", "150.00"),
                "stop": ("#.########", None),
                "atr": ("#.####%", None)
            }
            Then, 'key_validator' will return (["action", "type", "stop", "atr"], updated_data_settings)
        """
        key_none = []
        format_validator = DataFormatValidation(self.data_settings, self.input)

        if self.input:
            self.data_settings, _, _ = format_validator.get_results()
        for key, (fmt, value) in self.data_settings.items():
            if not value:
                key_none.append(key)
            if value in ["bulk", "action:bulk"]:
                self.bulk_mode()
        return key_none, self.data_settings

    def entry_loop(self):
        """
        Main loop to process trade entries, ensuring all required data is provided.

        This method starts the process of logging a trade. It continuously checks for any missing data
        in the data settings and prompts the user to provide the necessary information. Once all required
        data is collected, it calls the 'confirm_data' method to save the trade entry.

        Example:
            This method will prompt the user to enter values for the missing keys in 'data_settings',
            validate the input, and update 'data_settings' until all necessary information is provided.
        """
        print(TITLE("Starting to log a trade..."))

        Help(self.cmd).help_specifics()

        # Check if any string is None after validating input against formats/keys

        key_none, self.data_settings = self.key_validator()

        while True:
            if not key_none:
                break
            input_request = self.input_request(key_none)

            if input_request:
                # Merge new data with existing data settings

                new_data_settings, _ = input_request
                for k, v in new_data_settings.items():
                    if v[1] is not None:
                        self.data_settings[k] = v
                self.input = []
            else:
                break
            # Refresh Check if any string is None after validating input against formats/keys

            key_none, self.data_settings = self.key_validator()
        self.confirm_data()

    def input_request(self, key_none):
        """
        Request input from the user for the keys with None values.

        This method prompts the user to provide input for the keys that have not been provided with values.
        It validates the user input and updates the data settings accordingly. If the input is canceled,
        it returns False.

        Args:
            key_none (list): List of keys that need user input.

        Returns:
            tuple: Updated data_settings dictionary and prompt, or False if input is canceled.

        Example:
            If 'key_none' contains ["type", "price"], the method will prompt the user to enter values for
            these keys and update 'data_settings' with the new values.
        """
        while key_none:
            key = key_none[0]
            prompt = PATH(self.cmd, self.data_settings, key)
            input_validate = InputValidation(prompt, context=self.cmd)
            format_validator = DataFormatValidation(self.data_settings, prompt)

            if prompt:
                if not input_validate.multi_menu_call(silent=True):
                    new_data_details, _, _ = format_validator.get_results()

                    for k in self.data_settings:
                        if new_data_details[k][1] is not None:

                            # Ensure only key:value formatted data can update non-None values

                            if self.data_settings[k][1] is not None:
                                if ":" not in new_data_details[k][1]:
                                    continue
                                else:
                                    self.data_settings[k] = new_data_details[k]
                    return new_data_details, prompt
                else:
                    cancel = input_validate.multi_menu_call()
                    if cancel:
                        return False
            else:
                print(ERROR("Hey, that is empty! Try again please."))

    def bulk_mode(self):
        """
        Handle bulk mode import for trade entries.

        This method is called when the 'bulk' action is selected. It allows the user to import multiple
        trade entries in bulk.
        """
        print("Hey, you selected bulk-mode import!")

    def confirm_data(self):
        """
        Get confirmation from the user.

        This method prints the collected trade data for the user to review and confirm. If the user
        confirms the entries, it triggers saving the trade data.

        Example:
            The method will print the trade data in the format:
            "./entry action asset type price stop atr"
            It will then prompt the user to confirm the entries, and if confirmed, log the trade.
        """
        action, asset, type, price, stop, atr = (
            self.data_settings[k][1] for k in self.data_settings
        )

        print(green("\nTrade to be logged:"))
        print(f"./{self.cmd} {action} {asset} {type} {price} {stop} {atr}")
        confirmation = get_input(
            italic(green("Please confirm the entries above are correct (y/n):\n"))
        )
        confirmation = yes_or_no(confirmation)

        if confirmation:
            self.save_data()
            print(
                SUCCESS(
                    f"\nTrade stored with user input:\nentry {action} {asset} {type} {price} {stop} {atr}"
                )
            )
            Calculation.start()
        else:
            print(
                ERROR(
                    f"\nTrade cancelled:\nentry {action} {asset} {type} {price} {stop} {atr}"
                )
            )
            return False

    def save_data():
        print("save data to the DB")


class Help:
    """
    Provides methods to display help information and professional tips for using the command line interface
    effectively. This class helps users understand how to utilize various commands, handle input data, and
    navigate the application efficiently.

    Attributes:
        context (str): The name of the class to create an instance of, provided in lowercase.
        class_name (str): The capitalized class name derived from the context.
        instance (object): An instance of the class specified by the context.
    """

    def __init__(self, context=None):
        """
        Initializes the Help class with the specified context, creating an instance of the relevant class.

        Args:
            context (str): The name of the class to create an instance of, provided in lowercase.
        """
        self.context = context
        if isinstance(self.context, list):
            self.context = " ".join(self.context)
        self.class_name = (
            self.context.capitalize() if isinstance(self.context, str) else None
        )
        self.instance = (
            globals()[self.class_name]()
            if self.class_name and self.class_name in globals()
            else None
        )

    def help_specifics(self):
        """
        Print help and tips based on the current data settings.

        This method dynamically prints out the specifics for each key in the data settings of the specified
        class instance. It provides information about the order of data input and the options available for
        each key. Additional tips and guidelines are provided to help users understand how to input data
        correctly and efficiently.
        """
        # Introduce the section with an underlined and green-colored title

        print(underscore(green(f"\n\n{self.class_name} help and tips:")))

        data_settings = self.instance.data_settings
        # Get an iterator for the items of the dictionary

        item_iterator = iter(data_settings.items())

        # Extract the first item

        first_key, (_, _) = next(item_iterator)

        print(green(italic("\nCharacteristics:")))
        print("- The order of data input is: " + ", ".join(data_settings.keys()))

        for key, (format, value) in data_settings.items():
            format_text = "any value" if format == "any" else format
            print(f"- {key.capitalize()} options: {format_text}")
        print(green(italic("\nFunctionalities:")))
        print(
            "- You can still use any of the main menu calls, plese note that some of them might need to cancel the current job"
        )
        print(
            "- Some data can be autovalidated if they correctly match the format requested"
        )
        print(
            "- Invalid data that does not match any of the formats above will be automatically invalidated"
        )
        print(
            "- If too much data is input, only the first calls in the line will work, all extra ones are automatically invalidated"
        )
        print(
            "- If the Format accepts any characters, do not use spaces, that will only catch the first word before space"
        )
        print(
            "- The next data request in the line will prompt as a request, but you can still input valid data for other missing data"
        )
        print(
            "- The validated current data collection can be checked just above the prompt request"
        )
        print("- To edit any validated data use format data:value")
        print(dim(f"  Example: '{first_key}:value'"))
        print(
            "- Data using format 'any' can be forced from other input requests by using the edit option described above"
        )
        print(
            "- The data interpreter will try the best to match the input data, some type of inputs take precedence over others"
        )
        print(
            f"   1. Menu calls used force string ./ at the beggining e.g. './{self.context}'"
        )
        print(f"   2. Simple menu calls e.g. '{self.context}'")
        print(f"   3. Bulk mode")
        print(f"   4. Data using key-value format (e.g '{first_key}:value')")
        print(f"   5. Data that can be autovalidated as text input")
        print(f"   6. % values")
        print(f"   7. Numbers")
        print(
            "- Alert messages will advise of any invalidated data and request new input as needed"
        )

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
        print(
            "- Typing 'help' followed by another command will provide more details on that command"
        )
        print(dim("  Example: 'help entry'"))

        # Suggest starting with simple commands for newcomers

        print("- Allow some learning curve, and execute single commands at first")

        # Describe how to explicitly initiate main menu commands

        print(
            "- Adding './' to the start of a string forces it to be checked as main menu call"
        )
        print(dim("  Example: './entry"))

        # Provide examples on chaining commands and skipping ahead in workflows

        print("- You can also chain subcomands and skip steps ahead")
        print(dim("  Example: './entry open short'"))

        # Detail how the system prompts for missing data during operations

        print("- When running a job, you will be asked any missing data.")

        # Explain data input handling and validation

        print(
            "- If any data is requested, you can see all the data already input just above the command request"
        )
        print(
            dim(
                "  Example: './entry open short' will appear just above the input request after running this command"
            )
        )
        print(
            "- When inputting data you can use multiple strings on any order, the data will try validate it correctly"
        )
        print(
            dim("  Example: 'short ./entry open' or 'short entry open' will still work")
        )

        # Discuss forced data validation for specific subcommands

        print("- You can force data to be validated against a specific subcommand")
        print(dim("  Example: 'short ./entry action:open' or 'entry type:short open'"))

        # Highlight the requirement for declaring data types for certain entries

        print(
            "- Some data entries like 'asset:' in './entry' MUST be declared with it's data type"
        )
        print(
            dim(
                "  Example: 'short ./entry asset:SPY open', where 'SPY' alone would be invalid, but ok as 'asset:SPY'"
            )
        )

        # Illustrate how excess data input is managed

        print(
            "- Too much data input will be handled by validating what can be validated first in the order of entries and delete others"
        )
        print(
            dim(
                "  Example: 'short ./entry asset:SPY long', 'type' will be set to 'short' and 'long' will be removed as both are 'type'"
            )
        )

        # Explain how to update data once a subcommand is defined

        print(
            "- After some subcommand is defined, editting it can be done by inputting a forced declaration"
        )
        print(
            dim(
                "  Example: current validated data is './entry asset:SPY type:short', entering 'type:long' will update the previously set value"
            )
        )

    def help_loop(self):
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
        while True:
            if self.context is None:
                print(TITLE("Help Information:"))
                print("  - Type 'entry' to enter a trade")
                print("  - Type 'check' to view stats")
                print("  - Type 'set' to open settings")
                print("  - Type 'help' to get help")
                print("  - Type 'back' to return to previous location")
                print("  - Type 'cancel' to cancel current job")
                print("  - Type 'exit' to quit the program")
                print(
                    "\nCommands described above can be ran from anywhere in the program."
                )
                return False
            else:
                print(TITLE(f"Help for '{self.context}':"))

                if self.context not in ("check", "exit"):
                    self.help_specifics()
                print("\n-  Type 'back' or 'cancel' to return to where you were")
                print("-  Type 'help' again to see general help")

                cmd = PATH(f"help {self.context}")
                input_validate = InputValidation(cmd)

                if cmd == "back" or cmd == "cancel":
                    break
                elif input_validate.multi_menu_call(silent=True):
                    input_validate.multi_menu_call()
                else:
                    continue


class Set:
    def __init__(self):
        print("placeholder")


class Check:
    def __init__(self):
        print("placeholder")


## Process execution


class Calculation:
    def start(self):
        print("placeholder")


# Main loop


class TradingBookSystem:
    """
    This class encapsulates the main loop of the application, providing a command line interface
    to access various functionalities of the system. It continuously prompts the user for input
    and processes commands until the program is exited.

    Methods:
        run(): Executes the main loop, processing user commands indefinitely until an exit command
               is issued or the program is terminated.
    """

    def __init__(self):
        """
        Initializes the TradingBookSystem class, setting up the main menu and help tips.
        """
        self.menu = MainMenu()
        self.greeting = "\n\n\nWelcome to Trading Book System!"
        self.main_menu = list(self.menu.command.keys())

    def run(self):
        """
        Executes the main loop of the application, continuously prompting the user for input
        and processing commands until the program is exited. This loop is the primary interaction
        point for users, providing a command line interface to access various functionalities
        of the system.
        """
        # Greeting and instructions

        print(underscore(GREETING(self.greeting)))
        self.menu.menu_help()
        Help.pro_tips()

        global main_menu
        main_menu = self.main_menu

        # Loop requesting and processing inputs

        while True:
            cmd = PATH()
            if cmd:
                input_validate = InputValidation(cmd)
                input_validate.multi_menu_call()


if __name__ == "__main__":
    trading_book_system = TradingBookSystem()
    trading_book_system.run()
