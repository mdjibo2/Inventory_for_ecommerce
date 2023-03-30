import shopify
from config import Config

class ShopifyAPI:
    def __init__(self):
        shopify.ShopifyResource.set_site(Config.SHOPIFY_STORE_URL)
        shopify.ShopifyResource.set_credentials(
            Config.SHOPIFY_API_KEY,
            Config.SHOPIFY_API_PASSWORD
        )
    
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

