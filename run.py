import gspread
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
    print("Exiting the program...")
    exit()

def show_help():
    """
    Show help menu
    """
    print("Help Information:")
    print("  - Type 'add' to add trade")
    print("  - Type 'check' to view stats")
    print("  - Type 'set' to open settings")
    print("  - Type 'help' to get Help")
    print("  - Type 'exit' to quit the program.")

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
    print("\n\nWelcome to Trading Book System!\n")
    show_help()
    print("\n\nCall for 'help' if you need to see this menu again!")
    while True:
        cmd = get_input("Enter command: \n")
        if not process_command(cmd, trading_book):
            print("\033[31mUnknown command. Type 'help' for options.\033[0m")

# def menu_check(prompt, context=None):
#     """
#     Handle user input and allow navigation or continuation based on context. Also process cancellation requests.
#     """
#     while True:
#         input_value = get_input(prompt)
#         if input_value == 'help':
#             print(f"\n\nHelp for '{context}':")
#             print(" - Type 'back' to return to where you were")
#             print(" - Type 'cancel' to go back to main menu")
#             input_value = get_input("")
#             while True:
#                 if input_value == 'back':
#                     break 
#             continue
#         elif input_value == 'cancel':
#             if navigate_away() is None:
#                 return None
#         elif input_value in ('check','set','help'):
#             process_command(input_value, trading_book)
#         elif input_value in ('exit','add'):
#             if navigate_away() is None:
#                 return None
#         else:
#             return input_value


def menu_check(prompt, context=None):
    """
    Handle user input and allow navigation or continuation based on context. Also process cancellation requests.
    """
    initial_context=context
    while True:
        input_value = get_input(prompt)
        if input_value == 'help' and context != None:
            print(f"\n\nHelp for '{context}':")
            print(" - Type 'back' to return to where you were")
            print(" - Type 'cancel' to go back to main menu")
            input_value = get_input("")
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


def navigate_away():
    """
    Prompt confirmation request when moving away from running job
    """
    cancel = get_input("Navigating away will cancel the current job. Do you want to proceed? (y/n): \n")
    if cancel == 'y':
        return None
    elif cancel == 'n':
        return False
    else:
        print("\n\033[31mPlease use 'y' or 'n'.\033[0m")

                
def log_trade(trading_book, type=None, action=None, price=None, stop=None, atr=None):
    """
    Log a trade with optional user interaction for details.
    """
    print("\nStarting to log a trade...")
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
            value = menu_check(prompt, "trade")
            if value is None:
                print(f"Operation canceled during input for {key}.")
                return 
            trade_details[key] = (trade_details[key][0], value)  

    type, action, price, stop, atr = (trade_details[k][1] for k in trade_details)
    print(f"Logging trade with user input: Type={type}, Action={action}, Value={price}, Stop={stop}, ATR={atr}")


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