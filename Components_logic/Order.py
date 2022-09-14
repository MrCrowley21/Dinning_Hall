# describe objects of type Order
class Order:
    def __init__(self, order_id, items_nr, items_id, priority, max_wait, table_id):
        self.order_id = order_id
        self.items_nr = items_nr
        self.items_id = items_id
        self.priority = priority
        self.max_wait = max_wait
        self.table_id = table_id
