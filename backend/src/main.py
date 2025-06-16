"""
Main FastAPI Application Module

Implements API endpoints, WebSocket messaging, and integrates blockchain
with automatic peer syncing.

Author: LunaLynx12
"""

from routes import validators_route as validators_routes
from routes import blockchain_route as blockchain_routes
from routes import accounts_route as accounts_routes
from routes import messages_route as messages_routes
from routes import tests_route as tests_routes
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from routes import p2p_route as p2p_routes
from blockchain import get_blockchain
from local_database import init_db
from fastapi import FastAPI
import uvicorn
import asyncio


async def periodic_sync_task():
    """
    Periodically synchronizes the blockchain with peers every 60 seconds.

    The task waits 10 seconds before starting and then runs in an infinite loop.
    Currently only logs activity; actual P2P sync logic needs to be implemented.

    return: None
    """
    await asyncio.sleep(10)
    while True:
        print("[Background] Running periodic blockchain sync...")
        # TODO use p2p_route.py
        await asyncio.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application lifecycle events (startup and shutdown).

    On startup:
        - Initializes the local database
        - Starts the periodic blockchain synchronization task

    On shutdown:
        - Placeholder for cleanup operations (currently none)

    param app: The FastAPI application instance
    yield: Control is passed to the application
    """
    print("[Startup] Initializing database...")
    init_db()
    print("[Startup] Starting periodic blockchain sync task...")
    asyncio.create_task(periodic_sync_task())
    yield

app = FastAPI(lifespan=lifespan)
"""
FastAPI application instance with lifespan handler configured.

Registers all available route modules (routers) under their respective paths.
"""
app.include_router(blockchain_routes.router)
app.include_router(validators_routes.router)
app.include_router(accounts_routes.router)
app.include_router(p2p_routes.router)
app.include_router(tests_routes.router)
app.include_router(messages_routes.router)

bc = get_blockchain()
"""
Reference to the global blockchain instance used across the application.
"""

@app.get("/", include_in_schema=False)
async def index():
    """
    Root endpoint that redirects users to the API documentation page.

    return: RedirectResponse to /docs
    """
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    """
    Entry point for running the FastAPI application using Uvicorn.

    Starts the development server on localhost port 8000 with reload enabled.
    """
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)