# 🔐 Quantum-Safe Decentralized Chat on Blockchain

Welcome to a next-generation secure communication protocol—an end-to-end encrypted P2P chat system built on a **custom blockchain**, fortified with **post-quantum cryptography**, and engineered for **high-assurance communication** in decentralized networks.

---

## 🧠 System Overview

This project combines **cutting-edge cryptography**, **custom Proof-of-Authority blockchain consensus**, and **real-time communication** through GraphQL and WebSockets. Here's what powers it:

### Core Components:

| Layer              | Technology                    | Description                                                                 |
|-------------------|-------------------------------|-----------------------------------------------------------------------------|
| **Blockchain**     | Custom-made, PoA              | Immutable, synchronized ledger of events/messages across peers             |
| **P2P Network**    | WebSocket + Custom Discovery  | Direct peer discovery and messaging across a decentralized mesh            |
| **Crypto Stack**   | Dilithium + Kyber512 + AES-GCM| Post-quantum secure: Identity, key exchange, and message encryption        |
| **Transport Layer**| GraphQL over WebSocket        | Efficient, typed, and real-time message exchange                           |
| **Frontend**       | React + Next.js + TailwindCSS | Secure, modern UI for chat and identity display                            |

---

## 🚧 Technical Challenges

1. **Post-Quantum Security Integration**  
   Implementing NIST PQC algorithms (Kyber, Dilithium) into real-time P2P systems requires careful handling of key lifetimes, computational cost, and interoperability.

2. **Blockchain Synchronization**  
   Ensuring deterministic block propagation and state convergence using P2P syncing without central authority.

3. **Error Handling in P2P**  
   Malformed messages, invalid signatures, or corrupted keys must be detected and discarded **immediately** to preserve trust in decentralized communications.

4. **Scalability under Real-Time Constraints**  
   Achieving low-latency, encrypted messaging with chain validation in a decentralized environment—without compromising throughput.

---

## 🚀 Breakthrough Innovations

### ✅ Full PQC Handshake (Kyber + Dilithium)

A secure, decentralized identity/authentication protocol:

```mermaid
sequenceDiagram
    participant A as Alice (Initiator)
    participant B as Bob (Responder)

    A->>B: Send Public Key (Dilithium)
    B->>A: Verify Signature (Dilithium)

    A->>B: Send Kyber Encapsulated Key
    B->>A: Recover Shared Secret (Kyber Decapsulation)

    A->>B: AES-GCM Encrypted Message
    B->>A: Decrypt and Respond
```

### 🔗 Blockchain-Powered Message History

- **PoA consensus** avoids computational waste, ideal for controlled P2P environments.
- **GraphQL as data transport** ensures strong schema validation, real-time diff-sync, and typed messaging.
- Messages are stored as **signed, encrypted blocks** ensuring auditability and immutability.

---

## 🛠️ Implementation Roadmap

### ✅ Phase 1: Crypto & P2P Stack
- [x] Integrate `Dilithium` for identity verification
- [x] Implement ephemeral session keys using `Kyber512`
- [x] Establish `AES-GCM` symmetric layer for fast encrypted messaging
- [x] Real-time P2P over WebSocket
- [x] Error rejection and peer verification logic

### 🧪 Phase 2: Blockchain and Messaging Layer
- [x] PoA consensus for custom blockchain
- [x] Block propagation and sync via P2P
- [x] Message encapsulation in signed blocks
- [ ] Optimize GraphQL query/subscription schema

### 🎨 Phase 3: Frontend & User Flow
- [x] React/Next.js-based secure chat interface
- [x] Identity import/export
- [ ] Session rekeying logic
- [ ] UX for blockchain-backed message viewing

### 🔍 Risk Mitigation
- 🛡️ Cryptographic primitives modularized for upgradeability
- 🔁 Fallback mechanisms in handshake in case of peer failure
- 📈 Load simulations to test sync under growing node count

---

## 📘 Technical Notes

| FEATURE         | DILITHIUM              | KYBER                         |
|-----------------|------------------------|-------------------------------|
| Purpose         | Digital signatures     | Key exchange                  |
| Used for        | Identities, signing    | Secure session keys           |
| Long-term key?  | ✅ Yes                 | ❌ No                         |
| Example use case| Signing a transaction  | Securing a P2P connection     |
| Generates keys? | ✅ Yes (once per ID)   | ✅ Yes (per session)          |

### ❓ Why does Kyber generate keys?

Kyber **generates ephemeral key pairs** for establishing session-level secrets—not for long-term identity. This ensures forward secrecy in peer-to-peer messaging.

---

## 🔄 P2P Discovery and Secure Handshake

```mermaid
sequenceDiagram
    participant NodeA as Node A
    participant NodeB as Node B
    participant Discovery as Peer Discovery

    NodeA->>Discovery: Scan known ports/IPs
    Discovery-->>NodeA: Returns peer list

    NodeA->>NodeB: WebSocket Connect

    NodeA->>NodeB: Send Dilithium Public Key + Signature
    NodeB-->>NodeA: Verify Identity (Dilithium)

    NodeA->>NodeB: Send Kyber Encapsulated Shared Key
    NodeB-->>NodeA: Decapsulate to recover shared secret

    NodeA->>NodeB: AES-GCM Encrypted Message
    NodeB-->>NodeA: Decrypt and Respond
```

---

## 🧱 Optional: Blockchain-Backed Message History

```mermaid
sequenceDiagram
    participant NodeA as Node A
    participant NodeB as Node B
    participant Chain as Blockchain

    NodeA->>Chain: Create signed message block
    Chain-->>NodeA: Block accepted

    NodeA->>NodeB: Propagate encrypted block
    NodeB->>Chain: Add block to local chain
```

This design ensures **trustless, tamper-resistant storage** and seamless P2P propagation.

---

## 🥇 Competitive Advantage

- 💡 **Post-Quantum Resilience**: Fully compliant with NIST’s chosen PQC algorithms
- 🧩 **Composable Architecture**: Crypto, networking, and blockchain modules are independently swappable
- 📉 **Minimal Overhead**: PoA + P2P sync avoids blockchain bloat and PoW inefficiencies
- 🧬 **Schema-driven Transport**: GraphQL ensures error-resistant payloads

---

## 🔐 License

MIT License — use at your own risk; cryptography is hard, and security bugs are worse.
