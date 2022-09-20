# describe objects of type Order
class PreparedOrder:
    def __init__(self, received_order):
        self.order_id = received_order['order_id']
        self.table_id = received_order['table_id']
        self.waiter_id = received_order['waiter_id']
        self.items_id = received_order['items_id']
        self.priority = received_order['priority']
        self.max_wait = received_order['max_wait']
        self.pick_up_time = received_order['pick_up_time']
        self.cooking_time = received_order['cooking_time']
        self.cooking_details = received_order['cooking_details']
