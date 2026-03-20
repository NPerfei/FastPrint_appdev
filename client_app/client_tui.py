from colorama import init, Fore

from client_misc import *
from client_services import *

init(autoreset=True)

def submit_print_order():
    while True:
        try:
            print()

            print(create_print_order_header)

            print(Fore.CYAN + "\nType 0 at any point to exit the operation.")
            name = question_validate('Enter your name: ')
            no_pages = question_validate('How many pages to print: ', is_int=True)

            print()
            get_pricing()

            type = question_validate('Enter type of print (Select a number): ', is_int=True, validation_list=[1, 2, 3])

            match type:
                case 1: type = 'bw'
                case 2: type = 'colored'
                case 3: type = 'photo'

            assert isinstance(name, str)
            assert isinstance(no_pages, int)
            assert isinstance(type, str)

            create_order(name, no_pages, type)
            return
        except CustomExit:
            print(Fore.YELLOW + '[•] Exiting operation...')
            return
        except Exception as e:
            print(e)
            return


def change_order_status():
    while True:
        try:
            print()

            print(update_print_order_header)
            orders = list_orders()
            if not orders:
                print('Exiting operation...')
                return

            print(Fore.CYAN + "\nType 0 at any point to exit the operation.")
            id_to_change = question_validate('Enter ID of order to update (Select a number): ', is_int=True)
            
            assert isinstance(id_to_change, int)
            selected_order = get_order(id_to_change)
            
            assert isinstance(selected_order, dict)
            order_status = selected_order.get('status', None)
            if order_status == 'finished':
                show_result('This order is already finished and cannot be changed.', False)
                return
            if not order_status or order_status == 'cancelled':
                show_result('Order not found.', False)
                return
            
            primary_option = 'queued' if order_status == 'pending' else 'finished'

            print(f'[1] change to {primary_option} | [2] cancel order')
            new_status = question_validate('Choose new order status: ', is_int=True, validation_list=[1, 2])

            if new_status == 2:
                update_order_status(id_to_change, 'cancelled')
            else:
                update_order_status(id_to_change, primary_option)
        except CustomExit:
            print(Fore.YELLOW + '[•] Exiting operation...')
            return
        except Exception as e:
            print(Fore.YELLOW + "[•] An error occurred. Exiting operation...")
            return


def cancel_print_order():
    while True:
        try:
            print()
            
            print(cancel_print_order_header)
            orders = list_orders()
            if not orders:
                print('Exiting operation...')
                return

            print(Fore.CYAN + "\nType 0 at any point to exit the operation.")
            id_to_cancel = question_validate("Enter ID of order to cancel (Select a number): ", is_int=True)

            assert isinstance(id_to_cancel, int)
            cancel_order(id_to_cancel)
        except CustomExit:
            print(Fore.YELLOW + '[•] Exiting operation...')
            return
        except Exception as e:
            print(Fore.YELLOW + "[•] An error occurred. Exiting operation...")
            return


def view_orders():
    while True:
        try:
            print()
            
            print(view_menu_header)
            print(view_menu_input)

            inp = question_validate("Select an operation: ", is_int=True, validation_list=[1, 2, 3, 4, 5, 6])

            assert isinstance(inp, int)
            match inp:
                case 1: list_orders(True)
                case 2: list_orders(status='cancelled')
                case 3: list_orders(status='pending')
                case 4: list_orders(status='queued')
                case 5: list_orders(status='finished')
                case 6: return
        except CustomExit:
            return
        except Exception as e:
            print(Fore.YELLOW + "[•] An error occurred. Exiting operation...")
            return
        

def set_print_pricing():
    while True:
        try:
            print()
            print(set_print_pricing_header)

            get_pricing()
            
            print(Fore.CYAN + "\nType 0 at any point to exit the operation.")
            type = question_validate('Enter type of print to set price for (Select a number): ', is_int=True, validation_list=[1, 2, 3])

            match type:
                case 1: type = 'bw'
                case 2: type = 'colored'
                case 3: type = 'photo'

            new_price = question_validate(f'Enter new price for {type} print: ', is_float=True)
            
            assert isinstance(type, str)
            assert isinstance(new_price, float)

            update_pricing(type, new_price)
        except CustomExit:
            print(Fore.YELLOW + '[•] Exiting operation...')
            return
        except Exception as e:
                print(Fore.YELLOW + "[•] An error occurred. Exiting operation...")
                return


def display_print_pricing():
    print()
    print(display_print_pricing_header)
    get_pricing()

def main():
    while True:
        try:
            print('\n' + main_menu_header)

            print(main_menu_options)
            
            inp = question_validate('Select an operation: ', is_int=True, validation_list=[1, 2, 3, 4, 5, 6, 7, 8])

            assert isinstance(inp, int)
            match inp:
                case 1: view_orders()
                case 2: submit_print_order()
                case 3: change_order_status()
                case 4: cancel_print_order()
                case 5: display_print_pricing()
                case 6: set_print_pricing()
                case 7: clear_screen()
                case 8:
                    print(Fore.GREEN + "Exiting application. Bye bye!")
                    return
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[•] Abort signal received. Exiting application...")
            return

if __name__ == "__main__":
    clear_screen()
    main()