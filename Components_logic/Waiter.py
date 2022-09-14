import logging
from time import sleep
import random
from threading import Lock
import requests

from config import *

logging.basicConfig(level=logging.DEBUG)


class Waiter:
    def __init__(self, waiter_id, dinning_hall):
        self.waiter_id = waiter_id  # define the waite id
        self.dinning_hall = dinning_hall  # initiate the dinning hall configuration

    # simulate picking the order up process
    def pick_up_order(self, tables):
        while True:
            for table in tables:
                # picking up the orders if table is ready
                table.lock_order_state.acquire()
                if table.state == waiting_to_make_an_order:
                    order = self.get_the_order(table)
                    self.send_order(table, order)
                else:
                    table.lock_order_state.release()

    # simulate waiters actions toward a new table
    def get_the_order(self, table):
        # change state of table in waiting
        table.state = waiting_for_an_order_to_be_served
        table.lock_order_state.release()
        sleep(time_unit * random.randint(2, 4))  # set time for picking up the order
        order = table.pick_up_the_order()
        return order

    # notify the kitchen about new order arrival
    def send_order(self, table, order):
        # notify about order details
        logging.info(f'Waiter {self.waiter_id} is picking up the order from table {table.table_id} '
                     f'order {order.order_id}')
        requests.post(f'{kitchen_container_url}receive_order', json=order.__dict__)
        # notify about successful request to the kitchen
        logging.info(f'Order {order.order_id} has been sent to the Kitchen')
