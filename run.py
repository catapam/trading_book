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

def log_trade(trading_book, type=None, action=None, value=None, stop=None, atr=None):
    """
    Logic for logging a trade
    """
    # This going to be a class, just adding place holder
    if type and action and value and stop and atr:
        print("Trade logged successfully.\n")
    else:
        if not type:
            type = get_input("Enter trade type (long/short): \n")
        if not action:
            type = get_input("Enter action (open/close/update): \n")
        if not value:
            type = get_input("Enter value (#.##): \n")
        if not stop:
            type = get_input("Enter stop (#.##): \n")
        if not atr:
            type = get_input("Enter ATR (10.00% or 0.10): \n")
        print(f"Logging trade with user input: Type={type}, Action={action}, Value={value}, Stop-loss={stop}, ATR={atr}")

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