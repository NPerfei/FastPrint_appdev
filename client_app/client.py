from client_misc import *
from client_services import *
from colorama import init

import requests as req
import sys

init(autoreset=True)

price_map = {}


def view_orders():
    list_orders(True)
    print()

def viewprices():
    try:
        get_pricing()
        print()
    except Exception:
        pass

def search_by_id():
    try:
        if not arg_list: raise ValueError()
        id = arg_list[0]
        get_order(int(id), True)
    except ValueError:
        print(Fore.YELLOW + "Command format is: search [order id]")
        print(Fore.YELLOW + "  [order id] must be numerical.")
    except Exception:
        pass

def order():
    try:
        name, pages, p_type = arg_list[:3]
        pages = int(pages)

        total_cost = pages * price_map[p_type]

    
        create_order(name, pages, p_type)
        print(Fore.GREEN + f"Total Cost: ₱{total_cost}")
    except ValueError:
        print(Fore.YELLOW + "Command format is: order [name] [pages] [print type]")
        print(Fore.YELLOW + "  [pages] argument must ba a whole number.")
        print(Fore.YELLOW + f"  [print type] is any of the following: bw, colored, photo.")
    except Exception:
        pass

def get_print_prices(price_map: dict):
    try:
        r = req.get('http://127.0.0.1:8000/pricing')

        if r.status_code != 200: r.raise_for_status()

        data = r.json()

        for d in data:
            price_map[d['print_type']] = d['price_per_page']
    except req.ConnectionError as ce:
            show_result('Unable to connect to server. Check your internet connection and try again.', False)
    except req.HTTPError as httpe:
        status_code = httpe.response.status_code
        if status_code == 500:
            show_result('Sorry, the server is temporarily unable to handle your request.', False)
    except Exception:
        pass

get_print_prices(price_map)


try:
    operation = sys.argv[1]
    arg_list = sys.argv[2:]

    if not price_map:
        pass
    else:
        match operation:
            case 'order': order()
            case 'view': view_orders()
            case 'search': search_by_id()
            case 'viewprices': viewprices()
            case _:
                print(Fore.YELLOW + "Available commands are: order, view, search, viewprices.")

    if not operation or not arg_list:
        raise Exception()
except:
    print(Fore.YELLOW + "Available commands are: order, view, search, viewprices.")
