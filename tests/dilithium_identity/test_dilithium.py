from dilithium_py.dilithium import Dilithium2 as Dilithium
import base64
import os

# --- Key Serialization Utilities ---

def save_key(filename, key: bytes):
    with open(filename, "wb") as f:
        f.write(base64.b64encode(key))

def load_key(filename) -> bytes:
    with open(filename, "rb") as f:
        return base64.b64decode(f.read())

# --- Identity Management and Signing ---

def generate_identity():
    public_key, secret_key = Dilithium.keygen()
    print("[+] Keypair generated")
    save_key("dilithium_public.key", public_key)
    save_key("dilithium_secret.key", secret_key)
    print("[+] Keys saved to disk")
    return public_key, secret_key

def load_identity():
    public_key = load_key("dilithium_public.key")
    secret_key = load_key("dilithium_secret.key")
    print("[+] Keys loaded from disk")
    return public_key, secret_key

def sign_message(secret_key: bytes, message: bytes) -> bytes:
    signature = Dilithium.sign(secret_key, message)
    print("[+] Message signed")
    return signature

def verify_signature(public_key: bytes, message: bytes, signature: bytes) -> bool:
    is_valid = Dilithium.verify(public_key, message, signature)
    print(f"[+] Signature valid? {is_valid}")
    return is_valid

# --- Test Routine ---

def test_dilithium_identity():
    # If keys already exist, load them; else generate new
    if os.path.exists("dilithium_public.key") and os.path.exists("dilithium_secret.key"):
        pk, sk = load_identity()
    else:
        pk, sk = generate_identity()

    message = b"Hello, this is a quantum-safe signature."
    signature = sign_message(sk, message)

    # Print sizes
    print("[+] Public key size:", len(pk), "bytes")
    print("[+] Secret key size:", len(sk), "bytes")
    print("[+] Signature size:", len(signature), "bytes")
    
    verify_signature(pk, message, signature)

    tampered = b"Tampered message!"
    verify_signature(pk, tampered, signature)

if __name__ == "__main__":
    test_dilithium_identity()
