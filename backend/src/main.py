"""
Main FastAPI Application Module

Implements API endpoints, WebSocket messaging, and integrates blockchain
with automatic peer syncing.

Author: LunaLynx12
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from blockchain import get_blockchain, create_transaction
import uvicorn
import asyncio
from routes import tests_route as tests_routes
from routes import validators_route as validators_routes
from routes import accounts_route as accounts_routes
from routes import p2p_route as p2p_routes
from routes import blockchain_route as blockchain_routes
from routes import messages_route as messages_routes
from local_database import init_db

# --- Background Task ---
async def periodic_sync_task():
    await asyncio.sleep(10)  # Wait for services to start
    while True:
        print("[Background] Running periodic blockchain sync...")
        # TODO use p2p_route.py
        await asyncio.sleep(60)  # Sync every 60 seconds


# --- Lifespan Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("[Startup] Initializing database...")
    init_db()
    print("[Startup] Starting periodic blockchain sync task...")
    asyncio.create_task(periodic_sync_task())
    yield

# --- FastAPI Instance ---
app = FastAPI(lifespan=lifespan)
app.include_router(blockchain_routes.router)
app.include_router(validators_routes.router)
app.include_router(accounts_routes.router)
app.include_router(p2p_routes.router)
app.include_router(tests_routes.router)
app.include_router(messages_routes.router)
bc = get_blockchain()


# --- API Endpoints ---
@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)