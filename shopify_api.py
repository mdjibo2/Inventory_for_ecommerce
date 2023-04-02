import shopify
from config import Config

class ShopifyAPI:
    def __init__(self):
        self.session = shopify.Session(Config.SHOPIFY_STORE_URL, Config.SHOPIFY_API_VERSION)
        self.session.api_key = Config.SHOPIFY_API_KEY
        self.session.password = Config.SHOPIFY_PASSWORD
        self.shopify_resource = shopify
        self.shopify_resource.Session.setup(api_key=Config.SHOPIFY_API_KEY, secret=Config.SHOPIFY_SHARED_SECRET)

    def get_orders(self):
        orders = self.shopify_resource.Order.find()
        return orders
    
    def update_inventory_levels(self, product_id, inventory_quantity):
        product = shopify.Product.find(product_id)
        variant = product.variants()[0]
        variant.inventory_management = 'shopify'
        variant.inventory_quantity = inventory_quantity
        variant.save()

    def create_order(self, customer_email, line_items):
        order = shopify.Order()
        order.email = customer_email
        for item in line_items:
            variant = shopify.Variant.find(item['variant_id'])
            line_item = shopify.LineItem()
            line_item.variant_id = item['variant_id']
            line_item.quantity = item['quantity']
            line_item.price = variant.price
            order.line_items.append(line_item)
        order.save()
        return order.id

