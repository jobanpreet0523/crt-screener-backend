from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    tf = Column(String)
    min_price = Column(Integer)
    min_volume = Column(Integer)
    model = Column(String)
