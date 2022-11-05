# ports
ports = {
    'port_1': 8000,
    'port_2': 8001,
    'port_3': 8002,
    'port_4': 8003
}

# urls
urls_for_kitchen = {
    'kitchen_url_1': 'http://127.0.0.1:8080/',
    'kitchen_container_url_1': 'http://kitchen_container_1:8080/',
    'kitchen_url_2': 'http://127.0.0.1:8081/',
    'kitchen_container_url_2': 'http://kitchen_container_2:8081/',
    'kitchen_url_3': 'http://127.0.0.1:8082/',
    'kitchen_container_url_3': 'http://kitchen_container_3:8082/',
    'kitchen_url_4': 'http://127.0.0.1:8083/',
    'kitchen_container_url_4': 'http://kitchen_container_4:8083/'
}
food_ordering_url = 'http://127.0.0.1:5002/'
food_ordering_container_url = 'http://food_ordering_container:5002/'
# food_ordering = food_ordering_url
food_ordering = food_ordering_container_url

# table states
free = 0
waiting_to_make_an_order = 1
waiting_for_an_order_to_be_served = 2

# define constants
time_unit = 0.5
nr_tables = 6
nr_waiters = 3

# define configs according to the restaurants
restaurant_id = '1'
restaurant_name = 'Restaurant_' + restaurant_id
port = ports['port_' + restaurant_id]
dinning_hall_url = 'http://127.0.0.1:' + str(port) + '/'
dinning_hall_container_url = 'http://dinning_hall_container_' + restaurant_id + ':' + str(port) + '/'
kitchen_url = urls_for_kitchen['kitchen_url_' + restaurant_id]
kitchen_container_url = urls_for_kitchen['kitchen_container_url_' + restaurant_id]
# kitchen = kitchen_url
kitchen = kitchen_container_url
menu = 'dinning_hall_data/menu_' + restaurant_id + '.json'
# menu = 'dinning_hall_data/menu.json'
