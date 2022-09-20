# describe objects of type Order
class Order:
    def __init__(self, order_id, table_id, waiter_id, items_id, priority, max_wait):
        self.order_id = order_id
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.items_id = items_id
        self.priority = priority
        self.max_wait = max_wait
        self.pick_up_time = None
