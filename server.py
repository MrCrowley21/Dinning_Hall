from flask import Flask, request, jsonify

from Components_logic.Dinning_hall import *
from Components_logic.Table import *
from Components_logic.Waiter import *

# initialize the logger mode
logging.basicConfig(level=logging.DEBUG)

# initialize the server (app)
app = Flask(__name__)


# define server function to receive prepared orders from kitchen
@app.route('/receive_prepared_order', methods=['POST'])
def receive_prepared_order():
    prepared_order = request.json  # extract sent data
    logging.info(f'Prepared order {prepared_order["order_id"]} received for the table {prepared_order["table_id"]}')
    dinning_hall.provide_the_order(prepared_order)  # announce dinning hall about food arrival
    return jsonify(prepared_order)


# start the program execution
if __name__ == "__main__":
    # initialize server as a thread
    Thread(target=lambda: app.run(port=8000, host="0.0.0.0", debug=True, use_reloader=False)).start()
    # initialize dinning hall
    dinning_hall = DinningHall()
    dinning_hall.get_orders()
