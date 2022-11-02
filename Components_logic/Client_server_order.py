import time


class ClientServerOrder:
    def __init__(self, client_server_order, order_id):
        self.client_id = client_server_order['client_id']
        self.order_id = order_id
        self.is_ready = False
        self.estimated_waiting_time = 0
        self.items = client_server_order['items']
        self.priority = client_server_order['priority']
        self.max_wait = client_server_order['max_wait']
        self.created_time = client_server_order['created_time']
        self.prepared_time = None
        self.cooking_time = None
        self.cooking_details = None
