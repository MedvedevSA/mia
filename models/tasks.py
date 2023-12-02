from datetime import datetime, date

from sqlalchemy import ForeignKey, TIMESTAMP, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customer.id'))
    time_created: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    content: Mapped[dict] = mapped_column(JSON)
