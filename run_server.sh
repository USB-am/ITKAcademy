#!/bin/bash
python3.12 -m uvicorn app.main:application --host 127.0.0.1 --port 8000 --reload --loop asyncio