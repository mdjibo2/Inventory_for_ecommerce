import requests
from config import Config

class DolibarrAPI:
    def __init__(self):
        self.url = Config.DOLIBARR_API_URL
        self.key = Config.DOLIBARR_API_KEY

    def create_customer(self, customer):
        endpoint = f"{self.url}/thirdparties"
        headers = {'DOLAPIKEY': self.key}
        response = requests.post(endpoint, headers=headers, json=customer)
        return response.json()

    def create_invoice(self, invoice):
        endpoint = f"{self.url}/invoices"
        headers = {'DOLAPIKEY': self.key}
        response = requests.post(endpoint, headers=headers, json=invoice)
        return response.json()

