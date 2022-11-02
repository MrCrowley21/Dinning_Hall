from flask import Flask, request, jsonify
from copy import deepcopy

from Components_logic.Dinning_hall import *
from Components_logic.Table import *
from Components_logic.Waiter import *
from Components_logic.Prepared_order import *
from Components_logic.Client_server_order import *

# initialize the logger mode
logging.basicConfig(level=logging.DEBUG)

# initialize the server (app)
app = Flask(__name__)


# define server function to receive prepared orders from kitchen
@app.route('/receive_prepared_order', methods=['POST'])
def receive_prepared_order():
    received_order = request.json  # extract sent data
    prepared_order = PreparedOrder(received_order)
    logging.info(f'Prepared order {received_order["order_id"]} received for the table {received_order["table_id"]}')
    # dinning_hall.receive_the_order(prepared_order)  # announce dinning hall about food arrival
    Thread(target=dinning_hall.receive_the_order, args=(prepared_order,)).start()
    return jsonify(received_order)


@app.route('/v2/order', methods=['POST', 'GET'])
def receive_client_server_order():
    client_service_order = request.json  # extract sent data
    dinning_hall.lock.acquire()
    order_id = dinning_hall.order_id
    dinning_hall.order_id += 1
    dinning_hall.lock.release()
    order = ClientServerOrder(client_service_order, order_id)
    dinning_hall.lock.acquire()
    dinning_hall.client_server_orders[order_id] = order
    dinning_hall.lock.release()
    logging.info(f'New order received for the Client Service')
    kitchen_response = requests.post(f'{kitchen_url}receive_order', json=order.__dict__).json()
    registered_time = time.time()
    logging.info(f'{kitchen_response}')
    response = {'restaurant_id': restaurant_id, 'restaurant_address': dinning_hall_url,
                'order_id': order_id, 'estimated_waiting_time': kitchen_response['estimated_waiting_time'],
                'created_time': kitchen_response['created_time'], 'registered_time': registered_time}
    order.estimated_waiting_time = kitchen_response['estimated_waiting_time']
    return jsonify(response)


@app.route('/v2/order/<int:id_user>', methods=['GET'])
def get_order_state(id_user):
    dinning_hall.lock.acquire()
    order = deepcopy(dinning_hall.client_server_orders[id_user].__dict__)
    if dinning_hall.client_server_orders[id_user].is_ready:
        dinning_hall.lock.release()
    else:
        order_id = order['order_id']
        dinning_hall.lock.release()
        response = \
            requests.get(f'{kitchen_url}check_preparation/{order_id}').json()
        order['estimated_waiting_time'] = response['estimated_time']
    order.pop('client_id', None)
    order.pop('items', None)
    return jsonify(order)


@app.route('/update_data', methods=['GET'])
def update_restaurant_data():
    return {'rating': dinning_hall.rating_system.compute_average_mark(),
            'is_available': dinning_hall.is_available}


# start the program execution
if __name__ == "__main__":
    # initialize server as a thread
    Thread(target=lambda: app.run(port=port, host="0.0.0.0", debug=True, use_reloader=False)).start()
    # initialize dinning hall
    dinning_hall = DinningHall()
    dinning_hall.register_restaurant()
    dinning_hall.get_orders()
