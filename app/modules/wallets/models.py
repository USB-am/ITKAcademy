import uuid

from sqlalchemy import Uuid, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    balance: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
