from flask import Flask, request, jsonify

from shopify_api import ShopifyAPI
from front_accounting_api import FrontAccountingAPI

# Initialize Flask application
app = Flask(__name__)

# Initialize Shopify API client
shopify_api = ShopifyAPI()

# Initialize Front Accounting API client
front_accounting_api = FrontAccountingAPI()

# Define endpoint to create a new sales order on Shopify
@app.route('/api/sales_orders', methods=['POST'])
def create_shopify_order():
    # Get request data
    data = request.get_json()

    # Create order on Shopify
    order_id = shopify_api.create_order(data)

    # Return response data
    response_data = {'order_id': order_id}
    return jsonify(response_data)

# Define endpoint to update an existing sales order on Shopify
@app.route('/api/sales_orders/<order_id>', methods=['PUT'])
def update_shopify_order(order_id):
    # Get request data
    data = request.get_json()

    # Update order on Shopify
    shopify_api.update_order(order_id, data)

    # Return response data
    response_data = {'message': 'Order updated successfully'}
    return jsonify(response_data)

# Define endpoint to delete an existing sales order on Shopify
@app.route('/api/sales_orders/<order_id>', methods=['DELETE'])
def delete_shopify_order(order_id):
    # Delete order on Shopify
    shopify_api.delete_order(order_id)

    # Return response data
    response_data = {'message': 'Order deleted successfully'}
    return jsonify(response_data)

# Define endpoint to retrieve product information from Front Accounting
@app.route('/api/products')
def get_front_accounting_products():
    # Get product data from Front Accounting
    products = front_accounting_api.get_products()

    # Return product data as JSON
    return jsonify(products)

# Define endpoint to retrieve current inventory levels from Front Accounting
@app.route('/api/inventory')
def get_front_accounting_inventory_levels():
    # Get inventory levels from Front Accounting
    inventory_levels = front_accounting_api.get

