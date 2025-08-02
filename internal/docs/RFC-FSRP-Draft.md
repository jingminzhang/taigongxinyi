# RFC XXXX: Financial Semantic Routing Protocol (FSRP)

```
Network Working Group                                    J. Liao, Ed.
Request for Comments: XXXX                          Jixia Academy
Category: Standards Track                                July 2025
Obsoletes: None                                    ISSN: 2070-1721

                Financial Semantic Routing Protocol (FSRP)
```

## Abstract

This document defines the Financial Semantic Routing Protocol (FSRP), a novel application-layer protocol for distributed financial decision-making systems. FSRP enables semantic routing of financial information through multi-agent networks using ancient Chinese philosophical frameworks (Bagua) for state representation and consensus algorithms. The protocol addresses the lack of standardized communication mechanisms in modern AI-driven financial analysis systems.

## Status of This Memo

This Internet-Draft is submitted in full conformance with the provisions of BCP 78 and BCP 79.

This document is a product of the Jixia Academy Financial Protocol Working Group. Information about the current status of this document, any errata, and how to provide feedback on it may be obtained at https://github.com/jixia-academy/fsrp-spec.

## Copyright Notice

Copyright (c) 2025 IETF Trust and the persons identified as the document authors. All rights reserved.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Conventions and Definitions](#2-conventions-and-definitions)  
3. [Protocol Overview](#3-protocol-overview)
4. [Message Format](#4-message-format)
5. [Routing Algorithm](#5-routing-algorithm)
6. [Consensus Mechanism](#6-consensus-mechanism)
7. [Agent State Management](#7-agent-state-management)
8. [Security Considerations](#8-security-considerations)
9. [IANA Considerations](#9-iana-considerations)
10. [Implementation Guidelines](#10-implementation-guidelines)
11. [References](#11-references)
12. [Appendix](#12-appendix)

---

## 1. Introduction

### 1.1 Problem Statement

Current financial decision-making systems utilizing artificial intelligence and multi-agent architectures suffer from several critical limitations:

1. **Lack of Standardized Communication**: No standardized protocol exists for inter-agent communication in financial analysis networks
2. **Semantic Routing Deficiency**: Existing routing protocols do not consider the semantic content of financial information
3. **Consensus Mechanism Absence**: No established consensus algorithms for distributed financial decision-making
4. **Scalability Limitations**: Current systems cannot efficiently scale across multiple analytical domains

### 1.2 Solution Overview

FSRP addresses these limitations by providing:

- **Standardized Message Formats**: Well-defined protocol headers and payload structures for financial semantic data
- **Content-Aware Routing**: Routing algorithms that consider the semantic meaning of financial information
- **Distributed Consensus**: Byzantine fault-tolerant consensus mechanisms adapted for financial decision-making
- **Multi-Domain Support**: Extensible framework supporting multiple analytical domains (technical analysis, fundamental analysis, sentiment analysis, etc.)

### 1.3 Design Principles

FSRP is designed according to the following principles:

- **Semantic Awareness**: Routing decisions based on content semantics rather than just network topology
- **Cultural Integration**: Incorporation of ancient Chinese philosophical frameworks (I-Ching/Bagua) for state representation
- **Fault Tolerance**: Byzantine fault tolerance for consensus in adversarial financial environments
- **Extensibility**: Modular design allowing integration of new analytical domains
- **Efficiency**: Optimized for low-latency financial decision-making scenarios

---

## 2. Conventions and Definitions

### 2.1 Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

### 2.2 Terminology

**Agent**: An autonomous software entity capable of financial analysis and decision-making

**Bagua**: Eight trigrams from I-Ching representing fundamental states of change and decision

**Consensus Domain**: A logical grouping of agents participating in a specific consensus process

**Financial Semantic**: The meaning and context of financial information beyond its literal content

**Gua State**: A 3-bit representation of an agent's current analytical stance using Bagua encoding

**Routing Metric**: A numerical value representing the cost or preference for routing to a specific destination

**Wisdom Layer**: The protocol layer responsible for meta-analysis and reflection on agent decisions

---

## 3. Protocol Overview

### 3.1 FSRP Architecture

FSRP operates as a seven-layer protocol stack, mapping conceptually to the OSI model but optimized for financial semantic routing:

```
   +-------------------+
   |   Decision Layer  |  <- L7: Final investment decisions (Yuanshi)
   +-------------------+
   |   Wisdom Layer    |  <- L6: Meta-analysis and reflection (Sanqing)
   +-------------------+
   |   Session Layer   |  <- L5: Agent session management (AutoGen+MCP)
   +-------------------+
   |   Transport Layer |  <- L4: Data orchestration and flow control (N8N)
   +-------------------+
   |   Network Layer   |  <- L3: Semantic routing (RSS aggregation)
   +-------------------+
   |   Data Link Layer |  <- L2: Information framing (News processing)
   +-------------------+
   |   Physical Layer  |  <- L1: Event capture (World events)
   +-------------------+
```

### 3.2 Bagua State Representation

FSRP uses 8-state Bagua encoding for semantic state representation. Each state represents a fundamental analytical stance:

| Bagua Trigram | Binary | Decimal | Semantic Meaning | Financial Interpretation |
|---------------|--------|---------|------------------|--------------------------|
| Qian (乾)     | 111    | 7       | Creative Force   | Strong Bull Signal       |
| Dui (兑)      | 110    | 6       | Joyful Exchange  | Moderate Bull Signal     |
| Li (离)       | 101    | 5       | Clinging Fire    | Volatile Bull Signal     |
| Zhen (震)     | 100    | 4       | Arousing Thunder | Emerging Bull Signal     |
| Xun (巽)      | 011    | 3       | Gentle Wind      | Emerging Bear Signal     |
| Kan (坎)      | 010    | 2       | Abysmal Water    | Volatile Bear Signal     |
| Gen (艮)      | 001    | 1       | Keeping Still    | Moderate Bear Signal     |
| Kun (坤)      | 000    | 0       | Receptive Earth  | Strong Bear Signal       |

### 3.3 Network Topology

FSRP supports hierarchical network topologies with the following roles:

- **Leaf Agents**: Individual analytical agents (e.g., Eight Immortals, Twelve Generals)
- **Border Routers**: Domain aggregation points (e.g., Taishang Laojun)
- **Spine Routers**: Inter-domain routing (e.g., Lingbao Daojun)  
- **Root Controller**: Global orchestration (e.g., Yuanshi Tianzun)

---

## 4. Message Format

### 4.1 FSRP Header Format

All FSRP messages begin with a fixed 16-byte header:

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version|  Type |   Source Gua  |  Target Gua   |   Confidence  |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                          Timestamp                            |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Checksum            |            Reserved           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Field Descriptions:**

- **Version (4 bits)**: FSRP version number (current version: 1)
- **Type (4 bits)**: Message type (see Section 4.2)
- **Source Gua (3 bits)**: Source agent's current Bagua state
- **Target Gua (3 bits)**: Target agent's Bagua state or desired state
- **Confidence (6 bits)**: Confidence level (0-63, where 63 = 100% confidence)
- **Sequence Number (32 bits)**: Monotonically increasing sequence number
- **Timestamp (32 bits)**: Unix timestamp of message creation
- **Checksum (16 bits)**: Internet checksum of header and payload
- **Reserved (16 bits)**: Reserved for future use, MUST be zero

### 4.2 Message Types

FSRP defines the following message types:

| Type | Name | Description |
|------|------|-------------|
| 0 | FSRP_DATA | Financial semantic data payload |
| 1 | FSRP_CONTROL | Routing and control information |
| 2 | FSRP_CONSENSUS | Consensus protocol messages |
| 3 | FSRP_HEARTBEAT | Agent liveness and state updates |
| 4-15 | Reserved | Reserved for future use |

### 4.3 Payload Formats

#### 4.3.1 FSRP_DATA Payload

```json
{
  "analysis_type": "technical|fundamental|sentiment|risk",
  "symbol": "AAPL",
  "recommendation": {
    "action": "buy|sell|hold",
    "confidence": 0.85,
    "reasoning": "Technical breakout above resistance",
    "time_horizon": "short|medium|long"
  },
  "supporting_data": {
    "price": 175.43,
    "volume": 45234567,
    "indicators": {...}
  },
  "metadata": {
    "agent_id": "ludongbin_001",
    "domain": "jixia_academy",
    "timestamp": 1720598400
  }
}
```

#### 4.3.2 FSRP_CONSENSUS Payload

```json
{
  "phase": "propose|prepare|commit|finalize",
  "proposal_id": "uuid-string",
  "decision": {
    "symbol": "AAPL", 
    "action": "buy|sell",
    "confidence": 0.78,
    "rationale": "Consensus reached across 6/8 agents"
  },
  "votes": [
    {
      "agent_id": "ludongbin_001",
      "vote": "approve|reject",
      "gua_state": 7,
      "signature": "digital_signature"
    }
  ]
}
```

---

## 5. Routing Algorithm

### 5.1 Semantic Distance Calculation

FSRP routing decisions are based on semantic distance between Bagua states, calculated using the following algorithm:

```python
def calculate_semantic_distance(source_gua, target_gua):
    """
    Calculate semantic distance between Bagua states
    Based on I-Ching transformation principles
    """
    # XOR operation to find differing bits
    diff = source_gua ^ target_gua
    
    # Count number of different bits (Hamming distance)
    hamming_distance = bin(diff).count('1')
    
    # Apply I-Ching transformation weights
    transformation_weights = {
        0: 0.0,  # Same state
        1: 1.0,  # Single line change
        2: 1.5,  # Two line change  
        3: 2.0   # Complete transformation
    }
    
    return transformation_weights.get(hamming_distance, 3.0)
```

### 5.2 Routing Table Structure

Each FSRP agent maintains a routing table with the following structure:

| Destination Gua | Next Hop Agent | Metric | Interface | Age | Flags |
|-----------------|----------------|--------|-----------|-----|-------|
| 000 (Kun)       | hexiangu_001   | 1.0    | eth0      | 30s | U     |
| 001 (Gen)       | tieguaili_001  | 1.5    | eth1      | 45s | U     |
| 010 (Kan)       | ludongbin_001  | 2.0    | eth0      | 60s | U     |

**Field Descriptions:**
- **Destination Gua**: Target Bagua state
- **Next Hop Agent**: Next agent in routing path
- **Metric**: Routing cost (lower is better)
- **Interface**: Network interface identifier
- **Age**: Time since last update
- **Flags**: U=Up, D=Down, S=Static

### 5.3 Route Discovery Protocol

FSRP uses a proactive routing approach with periodic updates:

1. **Route Advertisement**: Agents periodically broadcast their reachable Gua states
2. **Distance Vector**: Each agent maintains distance vectors to all known Gua states
3. **Loop Prevention**: Split horizon with poison reverse to prevent routing loops
4. **Convergence**: Triggered updates for rapid convergence after topology changes

---

## 6. Consensus Mechanism

### 6.1 Bagua Byzantine Fault Tolerance (BBFT)

FSRP implements a modified Byzantine Fault Tolerance algorithm adapted for financial decision-making:

#### 6.1.1 Consensus Phases

**Phase 1: Proposal**
- Root Controller (Yuanshi) initiates consensus with investment proposal
- Proposal includes symbol, action, confidence threshold, and deadline

**Phase 2: Prepare**
- All participating agents analyze proposal using their domain expertise
- Agents broadcast PREPARE messages with their Gua state and preliminary vote

**Phase 3: Commit**
- If >2/3 of agents reach compatible Gua states, proceed to commit phase
- Agents broadcast COMMIT messages with final votes and digital signatures

**Phase 4: Finalize**
- Root Controller aggregates votes and announces final decision
- Decision is propagated to all agents and external systems

#### 6.1.2 Consensus Message Flow

```
Yuanshi (Root)     Sanqing (Processors)     Agents (Participants)
     |                     |                        |
     |--- PROPOSE -------->|                        |
     |                     |--- PREPARE ----------->|
     |                     |<-- PREPARE_ACK --------|
     |<-- PREPARE_RESULT --|                        |
     |--- COMMIT --------->|                        |
     |                     |--- COMMIT ------------>|
     |                     |<-- COMMIT_ACK ---------|
     |<-- COMMIT_RESULT ---|                        |
     |--- FINALIZE ------->|--- FINALIZE ---------->|
```

### 6.2 Fault Tolerance

FSRP consensus can tolerate up to f Byzantine failures where f < n/3 (n = total agents).

**Failure Detection:**
- Heartbeat messages every 30 seconds
- Timeout detection after 90 seconds
- Automatic exclusion of failed agents from consensus

**Recovery Mechanisms:**
- View change protocol for leader failures
- State synchronization for recovering agents
- Checkpoint and rollback for consistency

---

## 7. Agent State Management

### 7.1 Agent Lifecycle

FSRP agents follow a defined lifecycle:

1. **Initialization**: Agent starts and announces capabilities
2. **Discovery**: Agent discovers network topology and peers
3. **Active**: Agent participates in routing and consensus
4. **Maintenance**: Periodic state updates and health checks
5. **Shutdown**: Graceful departure with state cleanup

### 7.2 State Synchronization

Agents maintain synchronized state through:

- **Periodic Updates**: Broadcast current Gua state every 60 seconds
- **Triggered Updates**: Immediate broadcast on significant state changes
- **State Queries**: On-demand state requests between agents
- **Conflict Resolution**: Timestamp-based conflict resolution

### 7.3 Agent Registration

New agents join the network through the following process:

```json
{
  "message_type": "AGENT_REGISTER",
  "agent_info": {
    "agent_id": "unique_identifier",
    "agent_type": "technical|fundamental|sentiment|risk",
    "capabilities": ["stock_analysis", "options_analysis"],
    "domain": "jixia_academy",
    "version": "1.0.0"
  },
  "initial_gua_state": 4,
  "public_key": "agent_public_key"
}
```

---

## 8. Security Considerations

### 8.1 Authentication

FSRP requires strong authentication mechanisms:

- **Digital Signatures**: All consensus messages MUST be digitally signed
- **Public Key Infrastructure**: Agents MUST have valid certificates
- **Message Integrity**: Checksums MUST be verified for all messages
- **Replay Protection**: Sequence numbers MUST be monotonically increasing

### 8.2 Authorization

Access control is enforced through:

- **Role-Based Access**: Agents have defined roles (leaf, border, spine, root)
- **Domain Isolation**: Agents can only access their authorized domains
- **Capability Restrictions**: Agents limited to their declared capabilities

### 8.3 Privacy

Financial data privacy is protected through:

- **Payload Encryption**: Optional AES-256 encryption for sensitive data
- **Agent Anonymization**: Optional anonymization of agent identities
- **Audit Trails**: Comprehensive logging of all financial decisions

### 8.4 Threat Model

FSRP is designed to resist:

- **Byzantine Agents**: Malicious agents providing false information
- **Network Attacks**: Man-in-the-middle, replay, and DoS attacks  
- **Data Manipulation**: Unauthorized modification of financial data
- **Consensus Disruption**: Attempts to prevent consensus formation

---

## 9. IANA Considerations

### 9.1 Port Assignments

FSRP requires the following port assignments:

- **TCP Port 8888**: Reliable message delivery and consensus
- **UDP Port 8889**: Real-time market data and heartbeats
- **Multicast Address 224.0.1.88**: Consensus broadcast messages

### 9.2 Protocol Numbers

FSRP requests assignment of:
- **IP Protocol Number**: For direct IP encapsulation
- **Ethernet Type**: For Layer 2 implementations

### 9.3 Message Type Registry

IANA should maintain a registry of FSRP message types with the following initial assignments:

| Type | Name | Reference |
|------|------|-----------|
| 0 | FSRP_DATA | This document |
| 1 | FSRP_CONTROL | This document |
| 2 | FSRP_CONSENSUS | This document |
| 3 | FSRP_HEARTBEAT | This document |
| 4-15 | Reserved | This document |

---

## 10. Implementation Guidelines

### 10.1 Mandatory Features

Implementations MUST support:

- All 8 Bagua state representations
- BBFT consensus algorithm
- Message authentication and integrity checking
- Routing table maintenance
- Agent lifecycle management

### 10.2 Optional Features

Implementations MAY support:

- Payload encryption for privacy
- Message compression for efficiency
- Quality of Service (QoS) mechanisms
- Load balancing across multiple paths
- Advanced analytics and monitoring

### 10.3 Interoperability

To ensure interoperability:

- Implementations MUST follow the exact message formats specified
- Implementations MUST handle unknown message types gracefully
- Implementations SHOULD provide configuration options for timeouts
- Implementations SHOULD support protocol version negotiation

### 10.4 Performance Considerations

For optimal performance:

- Routing table updates SHOULD be rate-limited
- Consensus timeouts SHOULD be configurable
- Message queuing SHOULD be implemented for high-throughput scenarios
- Network topology SHOULD be optimized for low latency

---

## 11. References

### 11.1 Normative References

**[RFC2119]** Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119, March 1997.

**[RFC8174]** Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174, May 2017.

**[RFC5234]** Crocker, D., Ed., and P. Overell, "Augmented BNF for Syntax Specifications: ABNF", STD 68, RFC 5234, DOI 10.17487/RFC5234, January 2008.

### 11.2 Informative References

**[YIJING]** "I Ching: Book of Changes", Ancient Chinese text, circa 1000 BCE.

**[OSPF]** Moy, J., "OSPF Version 2", STD 54, RFC 2328, DOI 10.17487/RFC2328, April 1998.

**[BGP]** Rekhter, Y., Ed., Li, T., Ed., and S. Hares, Ed., "A Border Gateway Protocol 4 (BGP-4)", RFC 4271, DOI 10.17487/RFC4271, January 2006.

**[PBFT]** Castro, M. and B. Liskov, "Practical Byzantine Fault Tolerance", OSDI '99, February 1999.

---

## 12. Appendix

### 12.1 Example Message Exchange

```
Agent A (Gua State: 111) -> Agent B (Gua State: 000)

FSRP Header:
Version: 1, Type: 0 (DATA), Source Gua: 111, Target Gua: 000
Confidence: 45, Sequence: 12345, Timestamp: 1720598400
Checksum: 0xABCD, Reserved: 0x0000

Payload:
{
  "analysis_type": "technical",
  "symbol": "AAPL",
  "recommendation": {
    "action": "buy",
    "confidence": 0.85,
    "reasoning": "Bullish breakout pattern confirmed"
  }
}
```

### 12.2 Bagua Transformation Matrix

```
From\To  000  001  010  011  100  101  110  111
000      0.0  1.0  1.5  2.0  1.5  2.0  1.0  3.0
001      1.0  0.0  1.0  1.5  2.0  1.5  2.0  1.0
010      1.5  1.0  0.0  1.0  1.0  1.5  1.0  2.0
011      2.0  1.5  1.0  0.0  1.0  1.0  1.5  1.0
100      1.5  2.0  1.0  1.0  0.0  1.0  1.5  1.0
101      2.0  1.5  1.5  1.0  1.0  0.0  1.0  1.0
110      1.0  2.0  1.0  1.5  1.5  1.0  0.0  1.0
111      3.0  1.0  2.0  1.0  1.0  1.0  1.0  0.0
```

### 12.3 Implementation Checklist

- [ ] FSRP header parsing and generation
- [ ] Bagua state management
- [ ] Routing table implementation
- [ ] Consensus protocol implementation
- [ ] Security mechanisms (authentication, integrity)
- [ ] Agent lifecycle management
- [ ] Error handling and recovery
- [ ] Performance optimization
- [ ] Interoperability testing
- [ ] Documentation and examples

---

**Authors' Addresses**

J. Liao (Editor)  
Jixia Academy  
Email: liao@jixia.academy

---

*This document expires January 10, 2026*