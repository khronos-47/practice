from sqlalchemy import Column,  Integer, Numeric, String, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class parser_storage(Base):
    __tablename__ = "common_item"

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True,
    )
    ownership_form = Column(
        TEXT,
        nullable=False,
    )
    economic_activity = Column(
        TEXT,
        nullable=False,
    )
    number = Column(
        TEXT,
        nullable=False,
    )
    organization = Column(
        TEXT,
        nullable=False,
    )
    inn = Column(
        TEXT,
        nullable=False,
        index=True,
    )
    kpp = Column(
        TEXT,
        nullable=True,
        index=True,
    )
    address = Column(
        TEXT,
        nullable=True,
    )
    region = Column(
        TEXT,
        nullable=True,
    )
    phone = Column(
        TEXT,
        nullable = True,
    )
    email = Column(
        TEXT,
        nullable = True,
    )
    employee_count = Column(
        TEXT,
        nullable = True,
    )

    



