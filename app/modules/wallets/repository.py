from uuid import UUID
from decimal import Decimal

from sqlalchemy import select, update

from app.core.database import TSession
from app.modules.wallets.models import Wallet


class WalletRepository:
    def __init__(self, session: TSession):
        self.session = session

    async def get_wallet_for_update(self, uuid: UUID) -> Wallet:
        stmt = select(Wallet).where(Wallet.id == uuid).with_for_update()
        result = await self.session.execute(stmt)
        wallet = result.scalar_one_or_none()

        return wallet

    async def get_wallet(self, uuid: UUID) -> Wallet:
        stmt = select(Wallet).where(Wallet.id == uuid)
        result = await self.session.execute(stmt)
        wallet = result.scalar_one_or_none()

        return wallet

    async def update_wallet_balance(self, uuid: UUID, new_balance: Decimal) -> None:
        stmt = update(Wallet).where(Wallet.id == uuid).values(balance=new_balance)
        await self.session.execute(stmt)
