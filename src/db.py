import asyncpg
from fastapi import Request
import os


async def create_pool():
    return await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))


# Dependency to inject a connection into routes
async def get_connection(request: Request):
    async with request.app.state.pool.acquire() as conn:
        yield conn
