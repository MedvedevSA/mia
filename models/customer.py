from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Customer(Base):
    __tablename__ = 'customer'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone: Mapped[str] = mapped_column(VARCHAR(11))

    comment: Mapped[str]
