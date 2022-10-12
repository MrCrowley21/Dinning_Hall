import logging
from time import sleep, time
import random
from threading import Lock
import requests

from config import *

logging.basicConfig(level=logging.DEBUG)


class Waiter:
    def __init__(self, waiter_id, dinning_hall):
        self.waiter_id = waiter_id  # define the waite id
        self.dinning_hall = dinning_hall  # initiate the dinning hall configuration
        self.order_to_serve = []
        self.lock = Lock()

    # simulate picking the order up process
    def serve_tables(self, tables):
        while True:
            for table in tables:
                # picking up the orders if table is ready
                table.lock_order_state.acquire()
                if table.state == waiting_to_make_an_order:
                    table.generate_order(self.waiter_id)
                    pick_up_time = time()
                    order = self.get_the_order(table, pick_up_time)
                    self.send_order(table, order)
                else:
                    table.lock_order_state.release()
            while len(self.order_to_serve) > 0:
                current_order = self.order_to_serve[0]
                self.dinning_hall.tables[current_order.table_id - 1].receive_the_order(current_order)
                self.order_to_serve.pop(0)

    # simulate waiters actions toward a new table
    def get_the_order(self, table, pick_up_time):
        # change state of table in waiting
        table.state = waiting_for_an_order_to_be_served
        table.lock_order_state.release()
        sleep(time_unit * random.randint(2, 4))  # set time for picking up the order
        order = table.pick_up_the_order()
        order.pick_up_time = pick_up_time
        return order

    # notify the kitchen about new order arrival
    def send_order(self, table, order):
        # notify about order details
        logging.info(f'Waiter {self.waiter_id} is picking up the order from table {table.table_id} '
                     f'order {order.order_id}')
        requests.post(f'{kitchen_container_url}receive_order', json=order.__dict__)
        # notify about successful request to the kitchen
        logging.info(f'Order {order.order_id} with the following structure:\n'
                     f'{order.__dict__}\n has been sent to the Kitchen')
