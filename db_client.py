from typing import Optional, Type

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Define the base class for models
Base = declarative_base()

class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer)
    image = Column(String)
    category = Column(String)
    name = Column(String)
    price = Column(Float)
    discount = Column(Float)
    def __repr__(self):
        return f"<category={self.category}, name={self.name}, price={self.price}, discount={self.discount}, product_id={self.product_id}, image={self.image})>)>"

# DBClient class
class DBClient:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Create and return a new session"""
        return self.SessionLocal()

    def add_product(self, name: str, price: int, discount: str, product_id: str, image: str, category: int) -> Products:
        session = self.get_session()
        try:
            product = Products(name=name, price=price, product_id=product_id, image=image, category=category, discount=discount)
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
        except Exception as e:
            session.rollback()
            print(f"Error adding product: {e}")



