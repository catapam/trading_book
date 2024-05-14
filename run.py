import gspread
import re
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('trading_book')


main_menu=["entry","set","check","exit","help","cancel","back"]


def style_methods(cls):
    """
    This function creates a method that prints messages in the given color
    """
    for color_name, color_code in cls.colors.items():
        def color_func(message, color_code=color_code):
            return f"{color_code}{message}{cls.colors['none']}"
        setattr(cls, color_name, staticmethod(color_func))
    return cls


@style_methods
class StyleOutput:
    """
    Class to print messages in colored format based on ANSI escape codes.
    """
    colors={"red":"\033[31m",
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


red = StyleOutput.red
green = StyleOutput.green
bold = StyleOutput.bold
italic = StyleOutput.italic
underscore = StyleOutput.underscore
dim = StyleOutput.dim
GREETING = StyleOutput.orange
TITLE = StyleOutput.title
PATH = StyleOutput.gray
QUESTION = StyleOutput.cyan
SUCCESS= StyleOutput.green_background
ERROR= StyleOutput.error    

def exit_program():
    """
    Closes the program
    """
    # print("\n")
    print(ERROR("\nAll non-saved data will be lost"))
    leave = get_input(italic(red("Would you like to quit the program anyways? (y/n)\n")))
    confirmation = yes_or_no(leave)
    
    if confirmation is True:
        print("\nClosing...")
        print(GREETING("See you next time!"))
        exit()


def show_help(context=None):
    """
    Show help menu
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
            print(" - Type 'back' to return to where you were")
            print(" - Type 'cancel' to cancel current job and go back to main menu")
            print(" - Type 'help' again to see general help")
            cmd=get_input("\nEnter command: \n")
            
            if cmd == 'back':
                return False
            elif multi_menu_call(cmd,True):
                multi_menu_call(cmd,context="help")
            else:
                print(italic(red("\nNot a valid command!")))
                continue     
        
        
def process_command(cmd,child_command=None,context=None):
    """
    Process commands from command line
    """
    validator=True
    
    if cmd == "exit":
        validator = exit_program(*child_command) if child_command else exit_program()
    elif cmd == "check":
        validator = check_stats(*child_command) if child_command else check_stats()
    elif cmd == "help":
        if child_command:
            validator = show_help(*child_command)
        else:
            validator = show_help(context) if context else show_help()
    else:
        if not context:
            if cmd == "entry":
                validator = log_trade(*child_command) if child_command else log_trade()
            elif cmd == "set":
                validator = manage_settings(*child_command) if child_command else manage_settings()
            elif cmd == "cancel":
                validator = navigate_away()  
            elif cmd == "back":
                print(italic(red("\nThere is no where to go back to, you are in home page.")))
                print("Type 'help' to see menu options.")  
        else:
            if navigate_away() is True:
                print(SUCCESS("\nLet's continue with a new command!"))
                if cmd == "entry":
                    validator = log_trade(*child_command) if child_command else log_trade()
                elif cmd == "set":
                    validator = manage_settings(*child_command) if child_command else manage_settings()
            else:
                validator=False
                        
    return validator 


def get_input(prompt):
    """
    Get user's input to the command line
    """
    user_input = input(QUESTION(f"{prompt}"))
    return user_input.strip().lower()
           

def input_check(prompt,format=None):
    """
    Check if input is menu or not and push for format validations
    """
    if prompt is None:
        return None
    
    is_menu = multi_menu_call(prompt,True)
    if is_menu is True:
        return prompt
    else:
        if format is not None:
            format_is_valid = format_validation(prompt,format)
            return format_is_valid
        else:
            print("\n")
            print(ERROR("Invalid command."))
         

def multi_menu_call(prompt,check=False,context=None):
    """
    Checks user input for valid multi layer menu requests. 
    Check parameter is set as False by default, which runs the parent command request. 
    Passing the child_commands as parameters on the parent_command, and returning None if invalid.
    
    Setting check=True on the function call, will skip execution and simply return a validation response
    """
    if prompt:
        string_prompt = str(prompt)
        words = string_prompt.split()

        parent_command = ""
        child_command = []
        
        if 'help' in words:
            parent_command = "help"
        
        for word in words:
            if word in main_menu:
                if parent_command == "":
                    parent_command = word
                elif word != "help":
                    child_command.append(word)
            elif word != "help":
                child_command.append(word)
                        
        if parent_command in main_menu:
            validator = True
            if check == False:
                if process_command(parent_command,child_command,context=context) is False:
                    validator = False
        else:
            validator = False
        
        return validator


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
    

def navigate_away():
    """
    Prompt confirmation request when moving away from running job
    """
    cancel = get_input(italic(red("\nNavigating away will cancel the current job. Do you want to proceed? (y/n):\n")))
    return yes_or_no(cancel)
    
        
def yes_or_no(input):
    """
    Create the yes and no menu option for confirmation requests
    """
    while True:
        if input in ('y','yes','yeap','yeah','ya','ye','yy','yees','yess'):
            return True
        elif input in ('n','no','nope','nah','not','dont','nn','nno','noo'):
            return False
        else:
            print(ERROR("\nPlease use 'y' or 'n'."))
            input = get_input("\nEnter response:\n")
            continue
       

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
                
                if not multi_menu_call(prompt, True, context=cmd):
                    if len(words) <= len(key_none) + 1:
                        for word,key in zip(words,key_none):
                            fmt = trade_details[key][0]
                            trade_details[key] = (fmt,word)
                        key_none=[]
                        words=[]
                    else:
                        print("Too many arguments input, any extra arguments will be ignored.")
                        continue
                else:
                    if not multi_menu_call(prompt, context=cmd):
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


def delete_none_values(trade_details,num):
    """
    Deletes any None values from an array
    """
    trade_values = [value[num] for value in trade_details.values()]
    filtered_trade_values = [str(item) for item in trade_values if item is not None]
    
    return filtered_trade_values    

       
def view_stats():
    """
    Logic for viewing stats
    """
    print("Stats displayed successfully.")


def manage_settings():
    """
    Logic for managing settings
    """
    # This going to be a class, just adding place holder
    print("Settings updated successfully.")
    
    
def check_stats():
    """
    Check all trades active and curent stats of the trading strategy
    """
    print("Current Trading Stats:")
    
    
def main_loop():
    """
    Main loop initiating user input options
    """
    print(underscore(GREETING("\n\n\nWelcome to Trading Book System!")))
    show_help()
    print(underscore(green("\nTip:")))
    print("Typing 'help' followed by another command will provide more details on that command.")
    print("Example: 'help entry' or 'entry open short'")
    while True:
        cmd = get_input("\nEnter a valid command or 'help': \n")
        if cmd:
            if not multi_menu_call(input_check(cmd)):
                print(ERROR(""))

        
if __name__ == "__main__":
    main_loop()
    # print(red("test"))