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
from p2p_node import P2PNode
from fastapi import FastAPI
import argparse
import uvicorn
import asyncio
import config

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-port", type=int, default=8000, help="FastAPI server port")
    parser.add_argument("--peer-port", type=int, default=8762, help="P2P peer server port")
    return parser.parse_args()

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
        await p2p_routes.full_sync_endpoint()
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

    print(f"[Startup] Starting P2P node on port {config.peer_port}...")
    p2p_routes.p2p_node = P2PNode("127.0.0.1", config.peer_port)
    await p2p_routes.p2p_node.start()
    asyncio.create_task(p2p_routes.p2p_node.scan_for_peers())
    asyncio.create_task(periodic_sync_task())

    yield

    print("[Shutdown] Shutting down P2P node...")
    if hasattr(p2p_routes, "p2p_node"):
        await p2p_routes.p2p_node.server.ws_server.close()

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
    args = parse_args()

    # Override the global config ports
    config.api_port = args.api_port
    config.peer_port = args.peer_port

    print(f"[Main] Launching FastAPI server on port {args.api_port} with P2P on {args.peer_port}")
    uvicorn.run("main:app", host="127.0.0.1", port=args.api_port, reload=False)