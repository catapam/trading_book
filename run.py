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

def menu_check(prompt):
    """
    This function checks if the input is to navigate away or continue with the current job.
    It also handles cancellation requests interactively.
    """
    while True:
        input_value = get_input(prompt)
        if not process_command(input_value, SHEET):
            return input_value
        while True:  # Loop to handle cancellation verification
            cancel = get_input("\nNavigating away will cancel the current job. Do you want to proceed? (y/n): \n")
            if cancel.lower() == 'y':
                return None  # Return None to signal a cancellation
            elif cancel.lower() == 'n':
                break  # Exit the inner loop and re-prompt the original question
            else:
                print("\nPlease use 'y' or 'n'.")

def log_trade(trading_book, type=None, action=None, value=None, stop=None, atr=None):
    """
    Logic for logging a trade with optional user interaction to fill in details.
    """
    print("\nStarting to log a trade...")

    if not type:
        type = menu_check("Enter trade type (long/short): \n")
        if type is None:
            return 

    if not action:
        action = menu_check("Enter action (open/close/update): \n")
        if action is None:
            return

    if not value:
        value = menu_check("Enter value (#.##): \n")
        if value is None:
            return

    if not stop:
        stop = menu_check("Enter stop (#.##): \n")
        if stop is None:
            return 

    if not atr:
        atr = menu_check("Enter ATR (10.00% or 0.10): \n")
        if atr is None:
            return 

    print(f"Logging trade with user input: Type={type}, Action={action}, Value={value}, Stop={stop}, ATR={atr}")


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

main_loop(SHEET)