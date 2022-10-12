class ClientServerOrder:
    def __init__(self, client_server_order):
        self.items = client_server_order['items']
        self.priority = client_server_order['priority']
        self.max_wait = client_server_order['max_wait']
        self.created_time = client_server_order['created_time']
