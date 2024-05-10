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

def exit_program():
    """
    Closes the program
    """
    leave = get_input("\033[0mAll non-saved data will be lost\n\033[31mWould you like to quit the program anyways? (y/n)\n\033[0m")
    confirmation = yes_or_no(leave)
    if confirmation is True:
        print("\nClosing...\nSee you next time!")
        exit()


def show_help(context=None):
    """
    Show help menu
    """
    if context == "help":
        context=None
        
    initial_context=context
    
    while True:
        if context is None:
            print("\n\033[32mHelp Information:\033[0m")
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
            print(f"\n\033[32mHelp for '{context}':\033[0m")
            #context specifics placeholder
            print(" - Type 'back' to return to where you were")
            print(" - Type 'cancel' to cancel current job and go back to main menu")
            print(" - Type 'help' again to see general help")
            cmd=get_input("Enter command: \n")
            
            if cmd == 'back':
                return False
            elif multi_menu_call(cmd,True):
                multi_menu_call(cmd,context="help")
            else:
                print(f"\n\033[31mNot a valid command!\033[0m")
                continue     
        
        
def process_command(cmd,child_command=None,context=None):
    """
    Process commands from command line
    """
    validator=True
    
    if cmd == "exit":
        validator = exit_program(*child_command)
    elif cmd == "check":
        validator = check_stats(*child_command)
    elif cmd == "help":
        if child_command:
            validator = show_help(*child_command)
        else:
            validator = show_help(context)  
    else:
        if not context:
            if cmd == "entry":
                validator = log_trade(*child_command)
            elif cmd == "set":
                validator = manage_settings(*child_command)
            elif cmd == "cancel":
                validator = navigate_away()  
            elif cmd == "back":
                print("\033[31m\nThere is no where to go back to, you are in home page.\033[0m")
                print("Type 'help' to see menu options.")  
        else:
            if navigate_away() is True:
                print("\nLet's continue with a new command!")
                if cmd == "entry":
                    validator = log_trade(*child_command)
                elif cmd == "set":
                    validator = manage_settings(*child_command)
            else:
                validator=False
                        
    return validator 


def get_input(prompt):
    """
    Get user's input to the command line
    """
    user_input = input(f"\n\033[90m{prompt}\033[0m")
    return user_input.strip().lower()
           

def input_check(prompt,format=None):
    """
    Check if input is menu or not and push for format validations
    """
    is_menu = multi_menu_call(prompt,True)
    if is_menu is True:
        return prompt
    else:
        if format is not None:
            format_is_valid = format_validation(prompt,format)
            return format_is_valid
        else:
           print("\n\033[31mUnknown command. Type 'help' for options.\033[0m")
         

def multi_menu_call(prompt,check=False,context=None):
    """
    Checks user input for valid multi layer menu requests. 
    Check parameter is set as False by default, which runs the parent command request. 
    Passing the child_commands as parameters on the parent_command, and returning None if invalid.
    
    Setting check=True on the function call, will skip execution and simply return a validation response
    """
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

             
def format_validation(prompt,expected_format):
    """
    Checks input data for formatting issues
    """
    formats = {
    "open/close/update/bulk": {"format":"'open', 'close', 'update' or 'bulk'.",
                               "regex":'^(open|close|update|bulk)$'},
    
    "long/short": {"format":"'long' or 'short'",
                   "regex":'^(long|short)$'},
    
    "#.########": {"format":"a number with up to 8 decimal places, separated by dot.",
                   "regex":'^\\d+(\\.\\d{1,8})?$',
                   "decimal_places": 8},
    
    "#.####": {"format":"a number with up to 4 decimal places, separated by dot.\nThis is supposed to be a decimal notation. Example: 10% >> 0.10",
               "regex":'^\\d+(\\.\\d{1,4})?$',
               "decimal_places": 4}
    }

        # "template":{"format":None,
        #             "regex":None,
        #             "auto_validation":False,
        #             "decimal_places": 4},
    
    try:
        normalized_input = prompt.replace(',', '.')
        if normalized_input.startswith('.'):
            normalized_input = '0' + normalized_input

        for format_key, details in formats.items():
            if expected_format == format_key:
                if "decimal_places" in details:
                        number = float(normalized_input)
                        normalized_input = f"{number:.{details['decimal_places']}f}"

                if re.match(details["regex"], normalized_input):
                    return normalized_input
                else:
                    raise ValueError(f"Please enter a value in the format: {details['format']}")
                    
    except ValueError as e:
        print(f"\n\033[31mInvalid format detected: {prompt}")
        print(f"{e}\033[0m")
        

def navigate_away():
    """
    Prompt confirmation request when moving away from running job
    """
    cancel = get_input("\033[31mNavigating away will cancel the current job. Do you want to proceed? (y/n): \n\033[0m")
    return yes_or_no(cancel)
    
        
def yes_or_no(input):
    """
    Create the yes and no menu option for confirmation requests
    """
    try:
        while True:
            if input in ('y','yes','yeap','yeah','ya','ye','yy','yees','yess'):
                return True
            elif input in ('n','no','nope','nah','not','dont','nn','nno','noo'):
                return False
            else:
                raise ValueError(
                "\n\033[31mPlease use 'y' or 'n'.\033[0m"
                )
    except ValueError as e:
        print(f"{e}")
        
       
                
def log_trade(action=None, type=None, price=None, stop=None, atr=None):
    """
    Log a trade with optional user interaction for details.
    """
    print("\n\033[32mStarting to log a trade...\033[0m")
    stop_process = False
    bulk = False
    cmd="entry"
    
    trade_details = {
        "action": ("open/close/update/bulk", action),
        "type": ("long/short", type),
        "price": ("#.########", price),
        "stop": ("#.########", stop),
        "atr": ("#.####", atr)
    }
    
    for key in trade_details.keys():
        if trade_details[key][1] == "bulk":
            bulk = True
            break            
            
    if not bulk:    
        for key in trade_details.keys():
            format= trade_details[key][0]
            if trade_details[key][1] is not None:
                trade_details[key]= (format,format_validation(trade_details[key][1],format))
                
            if trade_details[key][1] is None:
                while True:
                    prompt = get_input(f"Enter trade {key} ({format}): \n")
                    if prompt == "bulk":
                        bulk = True
                        break
                    else:
                        if multi_menu_call(prompt,True,context=cmd) is False:
                            value = input_check(prompt, format)
                            if not value:
                                continue
                            else:
                                trade_details[key] = (format, value)
                                break
                        else:
                            if multi_menu_call(prompt,context=cmd) is False:
                                continue
                            else:
                                stop_process = True
                                break
                    
            if bulk or stop_process:
                break
            
        if stop_process or not bulk:       
            action, type, price, stop, atr = (trade_details[k][1] for k in trade_details)
            print(f"\033[32m\nLogging trade with user input: Action={action}, Type={type}, Value={price}, Stop={stop}, ATR={atr}\033[0m")
    
    if bulk: 
        print("Hey, you selected bulk-mode import!")
       
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
    print("\n\n\033[1m\033[38;5;208mWelcome to Trading Book System!\033[0m\n")
    show_help()
    print("\n\033[32mTip:\033[0m")
    print("Typing 'help' followed by another command will provide more details on that command.")
    print("Example: 'help entry' or 'entry open short'")
    while True:
        cmd = get_input("Enter command: \n")
        multi_menu_call(input_check(cmd))
        

main_loop()