import logging
from threading import Thread, Lock
import random
from time import sleep, time

from config import *
from Components_logic.Order import Order

logging.basicConfig(level=logging.DEBUG)


class Table:
    def __init__(self, table_id, dinning_hall):
        self.dinning_hall = dinning_hall  # initiate the dinning hall configuration
        self.table_id = table_id  # define the if of the table
        self.order = None  # define the current order of the table
        self.state = free  # define if the table is free, waiting for an order or received an order
        self.lock = dinning_hall.lock  # define the dining hall mutex
        self.lock_order_state = Lock()  # define the inner mutex

    # simulate the phase of occupying a table
    def occupy_the_table(self):
        logging.info(f'Table {self.table_id} is waiting for the clients...')  # notify table state
        # define time waiting for the clients
        sleep(time_unit * random.randint(3, 7))
        logging.info(f'Table {self.table_id} is done waiting...')  # notify table state
        # change table state
        self.state = waiting_to_make_an_order

    # simulate the phase of generating orders
    def generate_order(self, waiter_id):
        # set the id for the order and increment the counter
        with self.lock:
            order_id = self.dinning_hall.order_id
            self.dinning_hall.order_id += 1
        items_nr = random.randint(1, 10)  # set the number of items in the order
        # select the items and set related data
        items = random.choices(self.dinning_hall.foods, k=items_nr)
        # items_id = [i['id'] for i in items]
        items_id = [i['id'] for i in items]
        if items_nr < 10:
            priority = 5 - (items_nr // 2)  # set priority (by the number of orders)
        else:
            priority = 1
        max_wait = 1.3 * max(i['preparation-time'] for i in items)  # set the max waiting time for order receiving
        self.order = Order(order_id, self.table_id, waiter_id, items_id, priority, max_wait)
        # notify about item generation
        logging.info(f'Order {order_id} with {items_nr} items has been generated by the table {self.table_id}')

    # return the order that was picked up
    def pick_up_the_order(self):
        return self.order

    # simulate the phase of receiving the orders
    def receive_the_order(self, received_order):
        preparing_time = (time() - received_order.pick_up_time) / time_unit
        mark = self.dinning_hall.rating_system.get_mark(preparing_time, received_order.max_wait)
        average_mark = self.dinning_hall.rating_system.compute_average_mark()
        # set the absence of orders and free the table
        self.order = None
        self.state = free
        # notify about order receiving by the table
        logging.info(f'Order {received_order.order_id} has been received by the table {self.table_id}')
        logging.info(f'The mark given by the table {self.table_id} is {mark}. The average mark is: {average_mark}.'
                     f'Total preparing time: {preparing_time}. Desired time to wait: {received_order.max_wait}')
        Thread(target=self.occupy_the_table()).start()  # thread of table behaviour simulation
