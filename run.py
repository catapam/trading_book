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
trading_book = SHEET


def exit_program():
    """
    Closes the program
    """
    leave = get_input("\033[0mAll non-saved data will be lost\n\033[31mWould you like to quit the program anyways? (y/n)\n\033[0m")
    confirmation = yes_or_no(leave)
    if confirmation is None:
        print("\nClosing...\nSee you next time!")
        exit()


def show_help():
    """
    Show help menu
    """
    print("\n\033[32mHelp Information:\033[0m")
    print("  - Type 'add' to add trade")
    print("  - Type 'check' to view stats")
    print("  - Type 'set' to open settings")
    print("  - Type 'help' to get Help")
    print("  - Type 'cancel' to cancel current job")
    print("  - Type 'exit' to quit the program")
    print("\nCommands described here can be ran from anywhere in the program.")
    print("\n\033[32mTip:\033[0m")
    print("Typing 'help' followed by another command will provide more details on that command.")
    print("Example: 'help add'")


def check_stats(trading_book):
    """
    Check all trades active and curent stats of the trading strategy
    """
    trades = trading_book.get_all_open_trades()
    print("Current Trading Stats:")
    for trade in trades:
        print(trade)


def get_all_open_trades():
    """
    Get all open trades from database
    """
    # Placeholder


def process_command(cmd, trading_book):
    """
    Process commands from command line
    """
    if cmd == "exit":
        exit_program()
    elif cmd == "help":
        show_help()
    elif cmd == "check":
        check_stats(trading_book)
    elif cmd == "add":
        log_trade(trading_book)
    elif cmd == "set":
        manage_settings()
    else:
        return False 
    return True 


def get_input(prompt):
    """
    Get user's input to the command line
    """
    user_input = input(f"\n\033[90m{prompt}\033[0m")
    return user_input.strip().lower()


def main_loop(trading_book):
    """
    Main loop initiating user input options
    """
    print("\n\n\033[1m\033[38;5;208mWelcome to Trading Book System!\033[0m\n")
    show_help()
    while True:
        cmd = get_input("Enter command: \n")
        if not process_command(cmd, trading_book):
            print("\033[31mUnknown command. Type 'help' for options.\033[0m")


def menu_check(prompt, context=None):
    """
    Handle user input and allow navigation or continuation based on context. Also process cancellation requests.
    """
    initial_context=context
    while True:
        input_value = get_input(prompt)
        if input_value == 'help' and context != None:
            print(f"\n\033[32mHelp for '{context}':\033[0m")
            print(" - Type 'back' to return to where you were")
            print(" - Type 'cancel' to cancel current job and go back to main menu")
            print(" - Type 'help' again see general help")
            input_value = get_input("Enter command: \n")
            context = None

        if input_value == 'back':
            context=initial_context
            continue
        elif input_value == 'cancel':
            if navigate_away() is None:
                return None
        elif input_value in ('check','set','help'):
            process_command(input_value, trading_book)
        elif input_value in ('exit','add'):
            if navigate_away() is None:
                return None
        else:
            return input_value


def data_input_validation(prompt,expected_format,key,context=None):
    """
    Checks input data for formatting issues
    """
    try:
        while True:
            input_value = menu_check(prompt, context)
            if input_value is None:
                raise ValueError(
                    f"Operation canceled during input for {key}."
                    )

            if expected_format == "long/short":
                if re.match(r'^(long|short)$', input_value, re.IGNORECASE):
                    return input_value
                else:
                    raise ValueError(
                        "\033[31mPlease enter 'long' or 'short'.\033[0m"
                        )

            elif expected_format == "#.##":
                if re.match(r'^\d+(\.\d{1,2})?$', input_value):
                    return input_value
                else:
                    raise ValueError(
                        "\033[31mPlease enter a number with up to two decimal places, separated by dot.\033[0m"
                        )
                    
            elif expected_format == "open/close/update":
                if re.match(r'^(open|close|update)$', input_value, re.IGNORECASE):
                    return input_value
                else:
                    raise ValueError(                
                        "\033[31mPlease enter 'open' or 'close' or 'update'.\033[0m"
                        )
                    
    except ValueError as e:
        print(f"Invalid format:\n{e}")
        

def navigate_away():
    """
    Prompt confirmation request when moving away from running job
    """
    cancel = get_input("\033[31mNavigating away will cancel the current job. Do you want to proceed? (y/n): \n\033[0m")
    yes_or_no(cancel)
    
        
def yes_or_no(input):
    """
    Create the yes and no menu option for confirmation requests
    """
    if input in ('y','yes','yeap','yeah','ya','ye'):
        return None
    elif input in ('n','no','nope','nah','not','dont'):
        return False
    else:
        print("\n\033[31mPlease use 'y' or 'n'.\033[0m")
       
                
def log_trade(trading_book, type=None, action=None, price=None, stop=None, atr=None):
    """
    Log a trade with optional user interaction for details.
    """
    print("\n\033[32mStarting to log a trade...\033[0m")
    trade_details = {
        "type": ("long/short", type),
        "action": ("open/close/update", action),
        "price": ("#.##", price),
        "stop": ("#.##", stop),
        "atr": ("#.##", atr)
    }

    for key in trade_details.keys():
        while trade_details[key][1] is None:
            prompt = f"Enter trade {key} ({trade_details[key][0]}): \n"
            value = data_input_validation(prompt,trade_details[key][0],key,"trade")
            trade_details[key] = (trade_details[key][0], value)  

    type, action, price, stop, atr = (trade_details[k][1] for k in trade_details)
    print(f"\033[32mLogging trade with user input: Type={type}, Action={action}, Value={price}, Stop={stop}, ATR={atr}\033[0m")
       
       
def view_stats(trading_book):
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


main_loop(trading_book)