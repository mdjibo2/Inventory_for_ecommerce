from flask import Flask, request
from dolibarr_api import DolibarrAPI
from shopify_api import ShopifyAPI
from database import Database

app = Flask(__name__)

dolibarr_api = DolibarrAPI()
shopify_api = ShopifyAPI()
db = Database()

@app.route('/webhook/shopify/order_created', methods=['POST'])
def shopify_order_created():
    order_data = request.get_json()
    customer = {
        'name': f"{order_data['shipping_address']['first_name']} {order_data['shipping_address']['last_name']}",
        'email': order_data['email'],
        'phone': order_data['shipping_address']['phone'],
        'address': f"{order_data['shipping_address']['address1']} {order_data['shipping_address']['address2']}",
        'zip': order_data['shipping_address']['zip'],
        'city': order_data['shipping_address']['city'],
        'state_id': order_data['shipping_address']['province_code'],
        'country_id': order_data['shipping_address']['country_code']
    }
    dolibarr_customer = dolibarr_api.create_customer(customer)
    line_items = []
    for item in order_data['line_items']:
        variant_id = item['variant_id']
        quantity = item['quantity']
        line_items.append({'variant_id': variant_id, 'quantity': quantity})
        db.add_order(order_data['id'], customer['name'], item['price'])
    shopify_api.update_inventory_levels(variant_id, quantity)
    shopify_api.create_order(order_data['email'], line_items)
    return '', 200

@app.route('/webhook/dolibarr/inventory_updated', methods=['POST'])
def dolibarr_inventory_updated():
    inventory_data = request.get_json()
    product_id = inventory_data['product_id']
    inventory_level = inventory_data['inventory_level']
    db.update_product_inventory(product_id, inventory_level)
    shopify_api.update_inventory_levels(product_id, inventory_level)
    return '', 200

if __name__ == '__main__':
    app.run()

