import requests
from config import Config

class FrontAccountingAPI:
    def __init__(self):
        self.url = Config.FRONT_ACCOUNTING_API_URL
        self.key = Config.FRONT_ACCOUNTING_API_KEY
    
    def get_inventory_levels(self):
        response = requests.get(f'{self.url}/api/inventory?key={self.key}')
        if response.status_code == 200:
            return response.json()
        else:
            return None

