import time
from typing import List

import mysql.connector
import requests

from front_accounting_api import FrontAccountingAPI

# Initialize Front Accounting API client
front_accounting_api = FrontAccountingAPI()

# Initialize MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)

# Function to retrieve current inventory levels from Front Accounting API
def get_inventory_levels() -> List[dict]:
    inventory_levels = front_accounting_api.get_inventory_levels()
    return inventory_levels

# Function to update inventory levels in MySQL database
def update_inventory_levels(product_id: str, new_quantity: int) -> None:
    cursor = db.cursor()
    sql = "UPDATE products SET quantity = %s WHERE id = %s"
    val = (new_quantity, product_id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()

# Function to poll Front Accounting API for inventory updates and update the database
def poll_inventory_updates() -> None:
    while True:
        # Get current inventory levels
        inventory_levels = get_inventory_levels()

        # Loop through inventory levels and update the database
        for level in inventory_levels:
            product_id = level['product_id']
            quantity = level['quantity']

            update_inventory_levels(product_id, quantity)

        # Wait for next poll interval
        time.sleep(600)  # 10 minutes

if __name__ == '__main__':
    poll_inventory_updates()

