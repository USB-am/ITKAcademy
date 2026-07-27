from uuid import UUID
from decimal import Decimal

from fastapi import HTTPException

from app.core.database import TSession
from .repository import WalletRepository
from .utils import OperationType


class WalletService:
    def __init__(self, session: TSession):
        self.session = session
        self.repository = WalletRepository(session)

    async def change_balance(self, uuid: UUID, operation_type: OperationType, amount: Decimal) -> Decimal:
        wallet = await self.repository.get_wallet_for_update(uuid)

        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail='Wallet not found'
            )

        amount = abs(amount)
        if operation_type == OperationType.DEPOSIT:
            new_balance = wallet.balance + amount
        elif operation_type == OperationType.WITHDRAW:
            if wallet.balance < amount:
                raise HTTPException(
                    status_code=401,
                    detail='There are insufficient funds on the balance'
                )
            new_balance = wallet.balance - amount
        else:
            raise HTTPException(
                status_code=400,
                detail=f'Operation type "{operation_type}" is invalid!'
            )

        await self.repository.update_wallet_balance(uuid, new_balance)
        await self.session.commit()

        return new_balance

    async def get_balance(self, uuid: UUID) -> Decimal:
        wallet = await self.repository.get_wallet(uuid)

        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail='Wallet not found!'
            )

        return wallet.balance
