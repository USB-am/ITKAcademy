# -*- coding: utf-8 -*-

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.types import ASGIApp, Receive, Scope, Send

from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    print('lifespan func is started')
    yield
    print(f'lifespan func is finished')


application = FastAPI(lifespan=lifespan)
application.include_router(api_router)


class LogRequestsMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        start_time = time.perf_counter()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                process_time = (time.perf_counter() - start_time) * 1000
                print(f'Completed in {process_time:.2f}ms - Status: {status_code}')
            await send(message)
        await self.app(scope, receive, send_wrapper)


application.add_middleware(LogRequestsMiddleware)

