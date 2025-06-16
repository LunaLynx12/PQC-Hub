## Notes

- `Dilithium` is used for `digital signatures`
- `Kyber` is used for `key exchange` (not identities)


### So, why does Kyber generate keys?
- Because Kyber generates ephemeral key pairs for secure communication , not for long-term identity. 


|FEATURE|DILITHIUM|KYBER|
|---|---|---|
|Purpose|Digital signatures|Key exchange
|Used for|Identities, signing messages|Secure session keys
|Long-term key?|✅ Yes (identity stays the same)|❌ No (ephemeral for each session)
|Example use case|Signing a transaction|Securing a P2P connection
|Generates keys?|✅ Yes (once per identity)|✅ Yes (per session)

## Secure P2P Handshake Using Post-Quantum Crypto

```mermaid
sequenceDiagram
    participant A as Alice (Initiator)
    participant B as Bob (Responder)

    %% Step 1: Identity Exchange with Dilithium
    A->>B: Send Public Key (Dilithium)
    B->>A: Verify Signature (Dilithium)

    %% Step 2: Secure Key Exchange with Kyber
    A->>B: Send Kyber Encapsulated Key
    B->>A: Recover Shared Secret (Kyber Decapsulation)

    %% Step 3: Encrypt Messages using Shared Key
    A->>B: Send AES-256-GCM Encrypted Message
    B->>A: Decrypt & Respond with Encrypted Data

    Note right of A: Dilithium used to verify identity
    Note right of B: Kyber used to derive shared secret
    Note left of A: AES-256-GCM for message encryption
```

## Full P2P Network with Post-Quantum Identity, and Peer Discovery

```mermaid
sequenceDiagram
    participant NodeA as Node A
    participant NodeB as Node B
    participant Discovery as Peer Discovery

    title Secure Post-Quantum Chat Handshake

    Note left of NodeA: Node A scanning for peers...

    %% Step 0: Peer Discovery
    NodeA->>Discovery: Scan known ports/IPs
    Discovery-->>NodeA: Returns peer list

    NodeA->>NodeB: WebSocket Connect

    %% Step 1: Dilithium Identity Exchange
    NodeA->>NodeB: Send Dilithium Public Key + Signature
    NodeB-->>NodeA: Verify Identity (Dilithium)

    Note right of NodeB: Identity verified via\nDilithium digital signature

    %% Step 2: Kyber Key Exchange
    NodeA->>NodeB: Send Kyber Encapsulated Shared Key
    NodeB-->>NodeA: Decapsulate to recover same key

    Note right of NodeB: Shared secret established\nusing quantum-safe Kyber KEM

    %% Step 3: Secure Communication Layer
    NodeA->>NodeB: Send AES-256-GCM Encrypted Message
    NodeB-->>NodeA: Decrypt and Respond

    Note left of NodeA: All further communication\nuses symmetric encryption
```

## Optional Add-on: Web Interface with HTTPS
If you're adding a web UI (like Flask + HTML), you can show it in a separate flow like this:
```mermaid
sequenceDiagram
    participant User as User Browser
    participant WebUI as Web Server (Flask)
    participant LocalNode as Local Node

    title HTTPS for Local Web Interface

    User->>WebUI: HTTPS Request (TLS Secured)
    WebUI->>LocalNode: Communicate over localhost
    LocalNode-->>WebUI: Return chat data
    WebUI-->>User: Render chat page (HTTPS)

    Note right of User: TLS protects browser ↔ node interaction
```
This keeps TLS where it belongs — protecting the user’s connection to their own local node.
## Bonus: Add Blockchain Layer if Used for Message Storage
If you're storing messages in blocks on a blockchain:
```mermaid
sequenceDiagram
    participant NodeA as Node A
    participant NodeB as Node B
    participant Chain as Blockchain

    NodeA->>Chain: Create signed message block
    Chain-->>NodeA: Block accepted

    NodeA->>NodeB: Propagate encrypted block
    NodeB->>Chain: Add block to local chain

    Note right of Chain: Immutable message history
```

# DO NOT USE TLS in the P2P layer !!!!