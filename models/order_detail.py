from datetime import datetime

from sqlalchemy import ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class OrderDetail(Base):
    __tablename__ = 'order_detail'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    time_created: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    completion_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True
    )
    description: Mapped[str] = mapped_column(default='')
    cost: Mapped[int]
