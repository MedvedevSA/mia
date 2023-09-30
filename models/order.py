from datetime import datetime, date

from sqlalchemy import ForeignKey, TIMESTAMP, DATE, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customer.id'))
    time_created: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    due_date: Mapped[date] = mapped_column(DATE)
    completion_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True, default=None
    )
    comment: Mapped[str] = mapped_column(default='')
