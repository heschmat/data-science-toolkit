import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import false, true

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key= True)
    name = Column(String(100), nullable= false)


class MenuItem(Base):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key= True)
    name = Column(String(50), nullable= false)
    course = Column(String(50))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
