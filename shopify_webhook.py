import json
from dolibarr_api import DolibarrAPI
from shopify_api import ShopifyAPI
from flask import Flask, request

app = Flask(__name__)
dolibarr_api = DolibarrAPI()
shopify_api = ShopifyAPI()

@app.route('/webhooks/shopify/order/paid', methods=['POST'])
def handle_order_paid_webhook():
    data = request.get_data(as_text=True)
    order = json.loads(data)['order']
    customer_email = order['email']
    line_items = [{'variant_id': item['variant_id'], 'quantity': item['quantity']} for item in order['line_items']]
    dolibarr_customer = {
        'name': f"{order['billing_address']['first_name']} {order['billing_address']['last_name']}",
        'email': customer_email
    }
    dolibarr_invoice = {
        'thirdparty_id': dolibarr_api.create_customer(dolibarr_customer)['thirdparty']['id'],
        'line': [{'desc': item['title'], 'qty': item['quantity'], 'pu_ht': item['price']} for item in order['line_items']]
    }
    dolibarr_api.create_invoice(dolibarr_invoice)
    for item in line_items:
        shopify_api.update_inventory_levels(item['variant_id'], dolibarr_api.get_product_inventory(item['variant_id']))
    return 'OK'

