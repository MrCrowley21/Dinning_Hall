import threading
from threading import Thread
import logging
import requests
from time import time

from Components_logic.Menu import *
from Components_logic.Table import *
from Components_logic.Waiter import *
from Components_logic.Registration_data import *
from Components_logic.Rating_system import *

logging.basicConfig(level=logging.DEBUG)


class DinningHall:
    def __init__(self):
        self.restaurant_id = restaurant_id
        self.order_id = 1  # the order id
        self.foods = Menu().get_foods()  # list of foods in menu
        self.lock = threading.Lock()  # mutex variable
        # initialize list of tables with Table objects
        self.tables = [Table(i + 1, self) for i in range(nr_tables)]
        # initialize list of waiters with Waiter objects
        self.waiters = [Waiter(i + 1, self) for i in range(nr_waiters)]
        self.registration_data = RegistrationData()
        self.rating_system = RatingSystem()
        self.waiting_orders = []  # queue of orders waiting to be prepared
        self.max_capacity = 10  # max number of orders in buffer
        self.waiting_list_lock = Lock()  # the mutex on the buffer
        self.client_server_orders = {}  # the orders of clients from client server
        self.is_available = True

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
        self.waiting_list_lock.acquire()
        self.max_capacity += len(prepared_order.items_id)
        self.waiting_list_lock.release()
        if prepared_order.waiter_id is not None:
            current_waiter = self.waiters[prepared_order.waiter_id - 1]
            with current_waiter.lock:
                current_waiter.order_to_serve.append(prepared_order)
        else:
            self.lock.acquire()
            current_order = self.client_server_orders[prepared_order.order_id]
            current_order.prepared_time = time()
            current_order.is_ready = True
            current_order.cooking_time = prepared_order.cooking_time
            current_order.cooking_details = prepared_order.cooking_details
            current_order.estimated_waiting_time = 0
            self.lock.release()

    def register_restaurant(self):
        self.registration_data.menu_items = len(self.foods)
        self.registration_data.menu = self.foods
        self.registration_data.rating = self.rating_system.compute_average_mark()
        # send registration data
        requests.post(f'{food_ordering_url}register', json=self.registration_data.__dict__)
        logging.info(f'Restaurant {restaurant_id} send its registration data')
