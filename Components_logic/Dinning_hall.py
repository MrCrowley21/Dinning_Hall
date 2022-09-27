import threading
from threading import Thread
import logging
import requests

from Components_logic.Menu import *
from Components_logic.Table import *
from Components_logic.Waiter import *
from Components_logic.Rating_system import *

logging.basicConfig(level=logging.DEBUG)


class DinningHall:
    def __init__(self):
        self.order_id = 1  # the order id
        self.foods = Menu().get_foods()  # list of foods in menu
        self.lock = threading.Lock()  # mutex variable
        # initialize list of tables with Table objects
        self.tables = [Table(i + 1, self) for i in range(nr_tables)]
        # initialize list of waiters with Waiter objects
        self.waiters = [Waiter(i + 1, self) for i in range(nr_waiters)]
        self.rating_system = RatingSystem()

    # start the process of generating, picking up and sending the orders
    def get_orders(self):
        # announce the beginning of process execution
        logging.info(f'Searching for the orders')
        t = []  # list of threads for tables
        # start threads for the tables
        for i in range(len(self.tables)):
            t.append(Thread(target=self.tables[i].occupy_the_table()))
            t[i].start()
        for i in range(len(self.tables)):
            t[i].join()
        # start threads for waiters
        for waiter in self.waiters:
            Thread(target=waiter.serve_tables, args=(self.tables,)).start()

    # notify the table about food arrival
    def receive_the_order(self, prepared_order):
        # self.tables[prepared_order['table_id'] - 1].receive_the_order(prepared_order['order_id'],
        #                                                               prepared_order['max_wait'])
        current_waiter = self.waiters[prepared_order.waiter_id - 1]
        with current_waiter.lock:
            current_waiter.order_to_serve.append(prepared_order)
