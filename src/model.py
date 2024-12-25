
import uuid
from datetime import datetime
from sqlalchemy import Column, String,Float
from sqlalchemy.dialects.postgresql import UUID
from db import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)
    image = Column(String)
    price = Column(Float)