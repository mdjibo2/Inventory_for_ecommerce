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

