from sqlalchemy import Column,  Integer, Numeric, String, TEXT, DateTime
from project1.database.models import Base
from datetime import datetime

class log_entry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String)
    message = Column(String)