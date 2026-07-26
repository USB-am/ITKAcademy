# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.api.v1.router import api_router
# from app.modules.wallets import models
# from app.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(application: FastAPI):
    # await create_db_and_tables()
    print('lifespan func is started')
    yield
    print(f'lifespan func is finished')


application = FastAPI(lifespan=lifespan)
application.include_router(api_router)

# from core.config import auth
# auth.handle_errors(application)


@application.middleware('http')
async def log_requests(request: Request, call_next: Callable):
    start_time = datetime.now()

    response = await call_next(request)

    process_time = (datetime.now() - start_time).total_seconds() * 1000
    print(f'Completed in {process_time:.2f}ms - Status: {response.status_code}')
    return response
