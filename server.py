from flask import Flask, request, jsonify

from Components_logic.Dinning_hall import *
from Components_logic.Table import *
from Components_logic.Waiter import *
from Components_logic.Prepared_order import *

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
    dinning_hall.receive_the_order(prepared_order)  # announce dinning hall about food arrival
    return jsonify(received_order)


@app.route('/order', methods=['POST'])
def receive_client_server_order():
    client_service_order = request.json  # extract sent data
    logging.info(f'New order {client_service_order["order_id"]} received for the Client Service')
    return jsonify(client_service_order)


# start the program execution
if __name__ == "__main__":
    # initialize server as a thread
    Thread(target=lambda: app.run(port=port, host="0.0.0.0", debug=True, use_reloader=False)).start()
    # initialize dinning hall
    dinning_hall = DinningHall()
    dinning_hall.register_restaurant()
    dinning_hall.get_orders()
