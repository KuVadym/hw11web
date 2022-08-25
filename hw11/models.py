#Реализуйте хранение информации для вашего "Персонального помощника" в SQLite базе данных. 
# Реализуйте хранение книги контактов с email адресами, телефонами, именами в базе данных.

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

class Records(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    birth_date = Column(DateTime, default=None)
    address = Column(String(150), nullable=True)
    created = Column(DateTime, default=datetime.now())


class Emails(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=True, unique=True)
    record_id = Column(Integer, ForeignKey(Records.id, ondelete="CASCADE"))
    record = relationship("Records", backref="emails")

class Phones(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    phone= Column(Integer, nullable=True, unique=True)
    record_id = Column(Integer, ForeignKey(Records.id, ondelete="CASCADE"))
    record = relationship("Records", backref="phones")

