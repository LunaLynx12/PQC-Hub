# server.py
import asyncio
import websockets
import ssl
from pathlib import Path
from flask import Flask, send_from_directory

# Config
WS_PORT = 8765
HTTP_PORT = 8080
CERT_PATH = Path("certs")
CLIENTS = set()

# ---------------------------
# WebSocket Server (WSS)
# ---------------------------
async def handle_client(websocket):
    CLIENTS.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            # Broadcast to all clients
            if CLIENTS:
                await asyncio.gather(
                    *[client.send(f"[{id(websocket)}] {message}") for client in CLIENTS]
                )
    finally:
        CLIENTS.remove(websocket)

async def start_websocket_server():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(CERT_PATH / "cert.pem", CERT_PATH / "key.pem")

    async with websockets.serve(
        handle_client,
        "127.0.0.1",
        WS_PORT,
        ssl=ssl_context
    ):
        print(f"🔐 WSS server running on wss://127.0.0.1:{WS_PORT}")
        await asyncio.Future()  # Run forever

# ---------------------------
# Flask HTTP Server (for serving HTML)
# ---------------------------
app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

def start_flask_server():
    app.run(host="127.0.0.1", port=HTTP_PORT, ssl_context=None)
    print(f"🌐 HTTP server running on http://127.0.0.1:{HTTP_PORT}")

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    try:
        from threading import Thread

        # Start WebSocket server in background thread
        ws_thread = Thread(target=lambda: asyncio.run(start_websocket_server()), daemon=True)
        ws_thread.start()

        # Start Flask server in main thread
        start_flask_server()

    except KeyboardInterrupt:
        print("\nShutting down servers...")