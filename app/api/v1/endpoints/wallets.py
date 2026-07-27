from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter

from app.core.database import TSession
from app.modules.wallets.schemas import WalletResponse
from app.modules.wallets.models import Wallet
from app.modules.wallets.utils import OperationType
from app.modules.wallets.service import WalletService


wallets_router = APIRouter(prefix='/wallets', tags=['Wallets',])


@wallets_router.get(
    '/{wallet_id}',
    summary='Get wallet balance',
    description='Get wallet balance by wallet_id',
    response_model=WalletResponse)
async def get_wallet_balance(wallet_id: UUID, session: TSession):
    service = WalletService(session)
    balance = await service.get_balance(wallet_id)

    return WalletResponse(
        uuid=wallet_id,
        balance=balance
    )


@wallets_router.post(
    '/{wallet_id}/operation',
    summary='Update wallet balance',
    description='Send request to update Wallet.balance',
    response_model=WalletResponse)
async def post_wallet_operation(wallet_id: UUID,
                                amount: Decimal,
                                operation_type: OperationType,
                                session: TSession):

    service = WalletService(session)
    new_balance = await service.change_balance(
        uuid=wallet_id,
        operation_type=operation_type,
        amount=amount)

    return WalletResponse(
        uuid=wallet_id,
        balance=new_balance
    )


@wallets_router.post(
    '/add',
    summary='Add wallet',
    description='Add new Wallet to DB',
    response_model=WalletResponse)
async def add_new_wallet(session: TSession):
    new_wallet = Wallet()
    session.add(new_wallet)
    await session.commit()

    return WalletResponse(
        uuid=new_wallet.id,
        balance=new_wallet.balance
    )
