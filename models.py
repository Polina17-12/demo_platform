import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime
from database import Base

class Ticket(Base):
    __tablename__ = "tickets" 

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, nullable=False)
    status = Column(String, default="NEW", nullable=False)
    category_code = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))