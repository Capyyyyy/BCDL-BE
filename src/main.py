import asyncpg
import asyncio
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import uvicorn
from db import get_connection

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.pool = await asyncpg.create_pool(
        dsn=os.getenv("DATABASE_URL"),
        min_size=1,
        max_size=10,
        statement_cache_size=128  # or leave it out if using session mode
    )


    yield  # ⏸️ Here the app runs

    # Shutdown
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)


from routes import completions, levels, players
app.include_router(levels.router, prefix="/api")
app.include_router(players.router, prefix="/api")
app.include_router(completions.router, prefix="/api/levels")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3002))
    # Note: uvicorn.run() is great for simple testing. For production, it's better to
    # use a command-line process manager like Gunicorn with Uvicorn workers:
    # `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
    uvicorn.run(
        "__main__:app",  # More robust than "main:app" when run as a script
        host="0.0.0.0",
        port=port,
        reload=(os.getenv("APP_RELOAD", "false").lower() == "true"),
        workers=1
    )
