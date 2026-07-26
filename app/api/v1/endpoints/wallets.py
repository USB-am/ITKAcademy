from uuid import UUID
from typing import Literal
from enum import Enum

from fastapi import APIRouter

from app.modules.wallets.schemas import WalletResponse
from app.modules.wallets.models import Wallet


wallets_router = APIRouter(prefix='/wallets', tags=['Wallets',])


class OperationType(Enum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'


@wallets_router.get('/{wallet_id}', response_model=WalletResponse)
async def get_wallet_balance(wallet_id: UUID):
    balance = 1.0
    return WalletResponse(
        uuid=wallet_id,
        balance=balance
    )


@wallets_router.post('/{wallet_id}/operation')
async def post_wallet_operation(wallet_id: UUID,
                          amount: float,
                          operation_type: OperationType):

    if operation_type == OperationType.DEPOSIT:
        amount = abs(amount)

    elif operation_type == OperationType.WITHDRAW:
        amount = -abs(amount)

    return WalletResponse(
        uuid=wallet_id,
        balance=amount
    )


@wallets_router.post('/add', response_model=WalletResponse)
async def add_new_wallet():
    new_wallet = Wallet()
    return WalletResponse(
        uuid=new_wallet.id,
        balance=new_wallet.balance
    )
