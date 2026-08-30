# Product Requirements Document (PRD): ShadowNet Intelligence

## 1. Product Vision & Objective
ShadowNet is an evidence-grounded criminal intelligence and network analysis platform. It aims to convert heterogeneous, fragmented crime and investigation data into a connected, explainable knowledge system. By combining Knowledge Graphs, Graph Analytics, Machine Learning, NLP, RAG (Retrieval-Augmented Generation), and AI-assisted investigation, ShadowNet empowers investigators and analysts to discover hidden patterns, multi-hop relationships, and anomalous activities within vast datasets.

**Core Principle**: ShadowNet is an *intelligence-support system*, not an automated criminality-detection system. It highlights suspicious, anomalous, or noteworthy patterns but leaves the final conclusion to human investigators. All AI-generated insights must be grounded in actual database or document evidence.

## 2. Target Audience
* **Law Enforcement Investigators**: Detectives and officers who need to understand connections between suspects, locations, and crimes.
* **Financial Intelligence Analysts**: Analysts tracking money laundering and anomalous financial transactions.
* **Intelligence Officers**: Professionals uncovering organizational structures, communities, and illicit networks.

## 3. Key Use Cases
* **Network Exploration**: Discovering multi-hop relationships (e.g., Person A → CALLED → Person B → OWNS → Vehicle X → VISITED → Location Y).
* **Anomaly Detection**: Identifying unusual financial transactions based on amount, frequency, and time of day.
* **Timeline Reconstruction**: Viewing a chronological sequence of events (calls, transactions, FIRs) for a specific entity.
* **AI-Assisted Querying**: Asking natural language questions (e.g., "What connections does Person X have with Organization Y?") and receiving evidence-backed answers.
* **Unstructured Data Ingestion**: Automatically extracting entities and relationships from raw text documents like FIRs or field reports.

## 4. Features & Functional Requirements

### 4.1. Data Ingestion & Normalization
* **Requirement**: System must ingest data from various sources (FIRs, Transactions, Calls, Vehicles, Locations).
* **Requirement**: Data must be normalized into canonical schemas (Person, Phone, Vehicle, Location, Organization, Account, FIR, Crime, Event, Transaction).
* **Requirement**: Deduplication and entity resolution must occur to ensure unique identities.

### 4.2. Knowledge Graph (Core Engine)
* **Requirement**: Store normalized data as nodes and edges in a Neo4j graph database.
* **Requirement**: Support diverse node types and relationship types (e.g., `CALLED`, `USES_PHONE`, `HAS_ACCOUNT`, `MADE_TRANSACTION`).
* **Requirement**: Guarantee data integrity using `MERGE` and uniqueness constraints.

### 4.3. Graph Intelligence
* **Requirement**: Calculate **Degree Centrality** to find highly connected entities.
* **Requirement**: Calculate **Betweenness Centrality** to find bridge nodes between communities.
* **Requirement**: Calculate **PageRank** for structural importance.
* **Requirement**: Perform **Community Detection** to identify clustered groups within the network.
* **Future**: Shortest path, link prediction, Node2Vec, and advanced sub-graph detection.

### 4.4. Anomaly Detection (Machine Learning)
* **Requirement**: Utilize models (e.g., Isolation Forest) to score transactions for anomalies.
* **Requirement**: Extract features like transaction frequency, daily totals, time of day, and historical averages.
* **Requirement**: Output an anomaly score and a human-readable reason for the anomaly.

### 4.5. NLP Entity & Relationship Extraction
* **Requirement**: Process unstructured text (e.g., PDFs, FIRs) to extract entities (Persons, Locations) and relationships.
* **Requirement**: Map extracted data into structured JSON for graph ingestion.

### 4.6. RAG & Evidence-Grounded AI Agent
* **Requirement**: Provide a LangGraph/RAG-based AI assistant combining graph queries, vector search, and ML results.
* **Requirement**: Provide grounded responses with citations mapping directly back to source evidence.
* **Requirement**: The LLM must strictly be prevented from hallucinating or inventing relationships.

### 4.7. Investigation Dashboard (UI/UX)
* **Requirement**: Visual **Network Graph** interface for interactive exploration.
* **Requirement**: **Entity Profile View** (360-degree view of a person/entity).
* **Requirement**: **Investigation Timeline** to reconstruct events chronologically.
* **Requirement**: **Alerts Panel** for anomalous transactions and suspicious subgraph patterns.

## 5. System Architecture
The system adopts a multi-layered architecture:
1. **Data Ingestion Layer**: Python / FastAPI processing raw data.
2. **Normalization & Resolution Layer**: Deduplication, validation, canonical schema enforcement.
3. **Storage Layer**: 
    * Neo4j (Knowledge Graph)
    * Vector Database (for RAG)
    * Secure Storage (for raw evidence documents)
4. **Intelligence Layer**:
    * Graph Analytics Engine
    * ML Anomaly Detection (Isolation Forest)
    * NLP Pipeline (NER & Relation Extraction)
5. **API Layer**: FastAPI endpoints for UI and Agent communication.
6. **Presentation Layer**: React/TypeScript Web Dashboard.

## 6. Non-Functional Requirements
* **Security & Integrity**: Introduce an Evidence Hash mechanism (SHA-256) logged on an immutable ledger/audit log to prevent tampering.
* **Scalability**: Graph queries must be optimized to prevent runaway traversals (limit hop depth for general queries).
* **Explainability**: AI agent responses and anomaly scores must have transparent reasoning.

## 7. Milestones & Roadmap
* **M1 - M4**: Architecture, Normalization, Knowledge Graph, and Basic Graph Intelligence (✅ Completed)
* **M5**: Anomaly Detection pipeline setup (✅ Completed/In Progress)
* **M6 - M7**: Investigation Engine & Advanced Graph Intelligence (⏳ In Progress)
* **M8 - M9**: NLP Extraction & RAG Evidence-Grounded AI Agent (⏳ In Progress)
* **M10**: Investigation Timeline (✅ Completed/In Progress)
* **M11**: Evidence Integrity via Blockchain/Hashing (🔜 Planned)
* **M12**: Backend REST API (✅ Completed/In Progress)
* **M13**: Investigator Dashboard frontend UI (⏳ Partially Complete)
