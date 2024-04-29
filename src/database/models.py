from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    birthday = Column('birthday', Date)
    additional = Column(String(150), nullable=True)
