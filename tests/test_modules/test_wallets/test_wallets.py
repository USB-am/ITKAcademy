from typing import Any
from decimal import Decimal

import pytest
from httpx import AsyncClient

from app.modules.wallets.models import Wallet
from app.modules.wallets.utils import OperationType


@pytest.mark.asyncio
async def test_add_wallet(client: AsyncClient):
    response = await client.post('/api/v1/wallets/add')
    data = response.json()

    assert response.status_code == 201
    assert 'uuid' in data
    assert data['balance'] == 0.0


@pytest.mark.asyncio
@pytest.mark.parametrize('amount', (1, 50, 100.10, -53, '5.0'))
async def test_wallet_operation_deposit_positive(wallet: Wallet,
                                                 amount: int | float | str,
                                                 client: AsyncClient):
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        params={
            'amount': amount,
            'operation_type': OperationType.DEPOSIT.value,
        })
    data = response.json()

    assert response.status_code == 200
    assert Decimal(abs(float(amount))).quantize(Decimal('0.01')) == Decimal(str(data['balance']))


@pytest.mark.asyncio
@pytest.mark.parametrize('amount', (None, dict()))
async def test_wallet_operation_deposit_negative(wallet: Wallet,
                                                 amount: Any,
                                                 client: AsyncClient):
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        params={
            'amount': amount,
            'operation_type': OperationType.DEPOSIT.value,
        })
    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize('amount', (1, -50, 100.10, -53, '-5.0'))
async def test_wallet_operation_withdraw_positive(wallet: Wallet,
                                                  amount: int | float | str,
                                                  client: AsyncClient):
    await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        params={
            'amount': abs(float(amount)),
            'operation_type': OperationType.DEPOSIT.value,
        })
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        params={
            'amount': amount,
            'operation_type': OperationType.WITHDRAW.value,
        })
    data = response.json()

    assert response.status_code == 200
    assert Decimal('0.00') == Decimal(str(data['balance']))


@pytest.mark.asyncio
@pytest.mark.parametrize('amount', (5, 10, 15))
async def test_wallet_operation_withdraw_negative(wallet: Wallet,
                                                  amount: Any,
                                                  client: AsyncClient):
    await client.post(
            f'/api/v1/wallets/{wallet.id}/operation',
            params={
                'amount': abs(float(amount) - 1),
                'operation_type': OperationType.DEPOSIT.value,
            })
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        params={
            'amount': amount,
            'operation_type': OperationType.WITHDRAW.value,
        })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_wallet_operation_unknown_operation(wallet: Wallet,
                                                  client: AsyncClient):
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        params={
            'amount': 5,
            'operation_type': 'UnknownOperation',
        })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_wallet_balance(client: AsyncClient, wallet: Wallet):
    response = await client.get(f'/api/v1/wallets/{wallet.id}')
    data = response.json()

    assert response.status_code == 200
    assert float(data['balance']) == 0.0
    assert data['uuid'] == str(wallet.id)
