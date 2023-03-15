from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config
import datetime

Base = declarative_base()

class ProductInventory(Base):
    __tablename__ = 'product_inventory'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    inventory_level = Column(Float)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class Database:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
    
    def add_product_inventory(self, product_id, inventory_level):
        session = self.Session()
        product_inventory = ProductInventory(
            product_id=product_id,
            inventory_level=inventory_level
        )
        session.add(product_inventory)
        session.commit()
    
    def update_product_inventory(self, product_id, inventory_level):
        session = self.Session()
        product_inventory = session.query(ProductInventory).filter_by(product_id=product_id).first()
        if product_inventory:
            product_inventory.inventory_level = inventory_level
            product_inventory.last_updated = datetime.datetime.utcnow()
            session.commit()

