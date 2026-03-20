from typing import Any
from colorama import Fore

import os

class NotPositiveNumberError(Exception):
    def __init__(self, message="Must be a positive number.") -> None:
        super().__init__(message)


class CustomExit(Exception):
    def __init__(self, message="Use exited operation.") -> None:
        super().__init__(message)

def question_validate(question: str, is_int=False, is_float=False, validation_list: list | None = None):
    while True:
        try:
            inp = input(question).strip()

            if not inp:
                raise ValueError('Input cannot be empty.')
            
            if inp == '0':
                raise CustomExit()

            if is_int:
                inp = int(inp)
            if is_float:
                inp = float(inp)      
            if (is_int or is_float) and inp < 0: # type: ignore
                raise NotPositiveNumberError()
            
            if validation_list:
                if inp not in validation_list:
                    raise IndexError("Please choose from the list.")
            
            return inp
        except ValueError as ve:
            if is_int:
                show_result('Enter a whole number.', False)
            elif is_float:
                show_result('Enter a valid decimal number.', False)
            else:
                show_result(str(ve), False)
        except NotPositiveNumberError as npne:
            show_result(str(npne), False)
        except IndexError as ie:
            show_result(str(ie), False)


def show_result(message:str, is_ok=True):
    prepend = (Fore.GREEN + "[✓] ") if is_ok else (Fore.RED + "[X] ")
    output = prepend + message

    print(output)


def clean_data(data: list[dict[str, Any]] | dict[str, Any], include_id=False):
    if isinstance(data, list):
        for item in data:
                if include_id:
                    item.pop('id', None)
                item.pop('created_at', None)
                item.pop('updated_at', None)
    else:
        if include_id:
            data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# ---------------------------- Multi-line Messages -----------------------------
# Gi-lahi para dili kampat

main_menu_header = (
    Fore.MAGENTA + f"{'':=^112}\n" + Fore.RESET
    +
    Fore.CYAN + f"{'FastPrint - Your go to for printing solutions':^112}\n" + Fore.RESET
    +
    Fore.MAGENTA + f"{'':=^112}" + Fore.RESET
)

main_menu_options = '''[1] View Print Orders
[2] Create a Print Order
[3] Update Print Order Status
[4] Cancel a Print Order
[5] View Print Pricing
[6] Set Print Pricing
[7] Clear Screen
[8] Exit'''

view_menu_header = (
    Fore.CYAN + f"{'':=^66}\n" + Fore.RESET
    +
    f"{'View Orders':^66}\n" + Fore.RESET
    +
    Fore.CYAN + f"{'':=^66}" + Fore.RESET
)

view_menu_input ='''[1] View All Orders
[2] View Cancelled Orders
[3] View Pending Orders
[4] View Queued Orders
[5] View Finished Orders
[6] Exit'''

create_print_order_header = (
    Fore.CYAN + f"{'':=^66}\n" + Fore.RESET
    +
    f"{'Create Order':^66}\n" + Fore.RESET
    +
    Fore.CYAN + f"{'':=^66}" + Fore.RESET
)

update_print_order_header = (
    Fore.CYAN + f"{'':=^66}\n" + Fore.RESET
    +
    f"{'Update Order':^66}\n" + Fore.RESET
    +
    Fore.CYAN + f"{'':=^66}" + Fore.RESET
)

cancel_print_order_header = (
    Fore.CYAN + f"{'':=^66}\n" + Fore.RESET
    +
    f"{'Cancel Order':^66}\n" + Fore.RESET
    +
    Fore.CYAN + f"{'':=^66}" + Fore.RESET
)

set_print_pricing_header = (
    Fore.CYAN + f"{'':=^66}\n" + Fore.RESET
    +
    f"{'Set Print Pricing':^66}\n" + Fore.RESET
    +
    Fore.CYAN + f"{'':=^66}" + Fore.RESET
)

display_print_pricing_header = (
    Fore.CYAN + f"{'':=^66}\n" + Fore.RESET
    +
    f"{'Print Pricing':^66}\n" + Fore.RESET
    +
    Fore.CYAN + f"{'':=^66}" + Fore.RESET
)

