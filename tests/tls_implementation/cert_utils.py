from OpenSSL import crypto
from pathlib import Path

def generate_certs(output_dir: Path):
    """Generate CA and node certificates with SAN"""
    output_dir.mkdir(exist_ok=True)
    
    # Generate CA
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    cert = crypto.X509()
    cert.get_subject().CN = "P2P Test CA"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')
    
    # Save CA
    with open(output_dir / 'ca.pem', 'wb') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

    # Generate Node Cert with SAN
    node_key = crypto.PKey()
    node_key.generate_key(crypto.TYPE_RSA, 2048)
    node_cert = crypto.X509()
    node_cert.get_subject().CN = "localhost"
    
    # Add Subject Alternative Name
    san = crypto.X509Extension(
        b'subjectAltName',
        critical=False,
        value=b'DNS:localhost, IP:127.0.0.1'
    )
    node_cert.add_extensions([san])
    
    node_cert.set_serial_number(1001)
    node_cert.gmtime_adj_notBefore(0)
    node_cert.gmtime_adj_notAfter(365*24*60*60)
    node_cert.set_issuer(cert.get_subject())
    node_cert.set_pubkey(node_key)
    node_cert.sign(key, 'sha256')
    
    # Save Node Cert
    with open(output_dir / 'cert.pem', 'wb') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, node_cert))
    with open(output_dir / 'key.pem', 'wb') as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, node_key))