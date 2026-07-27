from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.modules.wallets.models import Wallet
from app.modules.wallets.utils import OperationType


@pytest.mark.asyncio
async def test_add_wallet(client: AsyncClient):
    response = await client.post("/api/v1/wallets/add")
    assert response.status_code == 201
    data = response.json()
    assert "uuid" in data
    assert data["balance"] == 0.0


@pytest.mark.asyncio
async def test_get_wallet_balance(client: AsyncClient, wallet: Wallet):
    response = await client.get(f"/api/v1/wallets/{wallet.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == str(wallet.id)
    assert float(data["balance"]) == 100.0


@pytest.mark.asyncio
async def test_get_wallet_not_found(client: AsyncClient):
    response = await client.get(f"/api/v1/wallets/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_deposit(client: AsyncClient, wallet: Wallet):
    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        params={
            "amount": "50.50",
            "operation_type": OperationType.DEPOSIT.value,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["balance"]) == 150.50


@pytest.mark.asyncio
async def test_withdraw(client: AsyncClient, wallet: Wallet):
    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        params={
            "amount": "30",
            "operation_type": OperationType.WITHDRAW.value,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["balance"]) == 70.0


@pytest.mark.asyncio
async def test_withdraw_insufficient_funds(client: AsyncClient, wallet: Wallet):
    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        params={
            "amount": "200",
            "operation_type": OperationType.WITHDRAW.value,
        },
    )
    assert response.status_code == 401
