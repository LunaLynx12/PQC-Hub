import asyncio
from pathlib import Path
from tls_node import TLSNode
from cert_utils import generate_certs

async def test_tls_connection():
    cert_path = Path('certs')
    generate_certs(cert_path)
    
    # Start server
    server = TLSNode("localhost", 8765, cert_path)  # Changed to localhost
    server_task = asyncio.create_task(server.start_server())
    
    await asyncio.sleep(1)
    
    # Test client connection
    await TLSNode.connect_to("localhost", 8765, cert_path)  # Changed to localhost
    
    server_task.cancel()

if __name__ == "__main__":
    asyncio.run(test_tls_connection())