from colorama import Fore
from client_misc import *

import requests as req

server_url = 'http://127.0.0.1:8000'

def handle_requests_errors(func):
    """Decorator function for standardized requests module error handling"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print(Fore.LIGHTBLACK_EX + '\nSending request to server...')
            return func(*args, **kwargs)
        except req.ConnectionError as ce:
            show_result('Unable to connect to server. Check your internet connection and try again.', False)
            raise ce
        except req.HTTPError as httpe:
            status_code = httpe.response.status_code
            if status_code == 422:
                show_result('The provided data was invalid', False)
            elif status_code == 404:
                show_result('Requested data was not found.', False)
            elif status_code == 500:
                show_result('Sorry, the server is temporarily unable to handle your request.', False)
            raise httpe

    return wrapper


@handle_requests_errors
def list_orders(all = False, status: str = "") -> bool:
    if not status:
        r = req.get(server_url + '/orders')
    else:
        r = req.get(server_url + '/orders', params={'status': status})
    if r.status_code != 200: r.raise_for_status()

    data = r.json()
    
    if not all and not status:
        data = [d for d in data if d['status'] not in ('finished', 'cancelled')]
    
    print()
    print(Fore.YELLOW + f"{'Print Orders':=^40}")
    if not data:
        print(Fore.YELLOW + f"{'There are no print orders...':^40}")
        return False

    clean_data(data)
    for d in data:
        print(f'    {d['id']}| {d['customer_name']:<30}| pages: {d['pages']:<9}| type: {d['print_type']:<8}| total: ₱{d['cost']:<9}| status: {d['status']:<10}|')
    
    return True

@handle_requests_errors
def get_order(order_id: int): # need to add response status checking for this and also other services
    r = req.get(server_url + f'/orders/{order_id}')
    if r.status_code != 200: r.raise_for_status()

    data = r.json()
    clean_data(data, True)

    
    return data
    # print(f'{data['customer_name']:<30}| pages: {data['pages']:<9}| type: {data['print_type']:<8}| total: ₱{data['cost']:<9}| status: {data['status']:<10}|')
    
@handle_requests_errors
def get_pricing():
    r = req.get(server_url + '/pricing')
    if r.status_code != 200: r.raise_for_status()

    data = r.json()

    clean_data(data, True)
    count = 1
    
    print(Fore.YELLOW + f"{'Print Prices':=^40}")
    for d in data:
        print(f'[{count}] {d['print_type']:<8}: ₱{d['price_per_page']}\t')
        count += 1

@handle_requests_errors
def create_order(customer_name: str, pages: int, print_type: str):
    payload = { "customer_name": customer_name, "pages": pages, "print_type": print_type }
    r = req.post(server_url + '/orders', json=payload)
    
    if r.status_code == 200:
        show_result('Order successfully placed.')
    else:
        show_result('Order creation failed.', False)
    if r.status_code != 200: r.raise_for_status()

@handle_requests_errors
def cancel_order(order_id: int):
    r = req.delete(server_url + f'/orders/{order_id}')

    if r.status_code == 200:
        show_result('Successfully cancelled order.')
    else:
        show_result('Unable to cancel order.', False)
    if r.status_code != 200: r.raise_for_status()

@handle_requests_errors
def update_order_status(order_id: int, status: str):
    payload = { "status": status }
    r = req.patch(server_url + f'/orders/{order_id}/status', json=payload)

    if r.status_code == 200:
        show_result(f'Order status updated to {status}.')
    else:
        show_result('Failed to update order status.', False)
    if r.status_code != 200: r.raise_for_status()

@handle_requests_errors
def update_pricing(print_type: str, new_price: float):
    payload = { "print_type": print_type, "price_per_page": new_price }
    r = req.put(server_url + f'/pricing/{print_type}', json=payload)

    if r.status_code == 200:
        show_result(f'Price per page for {print_type} prints updated successfully.')
    else:
        show_result('Failed to update price.', False)
    if r.status_code != 200: r.raise_for_status()