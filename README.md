# ShadowNet

> **An evidence-grounded criminal intelligence and network analysis platform combining Knowledge Graphs, Graph Analytics, Machine Learning, NLP, RAG, and AI-assisted investigation.**

---

## 📌 Project Status

**Current implementation:**

| Milestone | Component                         | Status      |
| --------- | --------------------------------- | ----------  |
| M1        | Problem Definition + Architecture | ✅ Complete |
| M2        | Data Inspection + Normalization   | ✅ Complete |
| M3        | Knowledge Graph                   | ✅ Complete |
| M4        | Graph Intelligence                | ✅ Complete |
| M5        | Anomaly Detection                 | ✅ Complete |
| M6        | Investigation Engine              | ✅ Complete |
| M7        | Advanced Graph Intelligence       | ✅ Complete |
| M8        | NLP Entity + Relation Extraction  | ✅ Complete |
| M9        | RAG + Evidence-Grounded AI Agent  | ✅ Complete |
| M10       | Investigation Timeline            | ✅ Complete |
| M12       | Backend API                       | ✅ Complete |
| M13       | Investigator Dashboard            | partially Complete  |

The repository is currently focused on building the **core intelligence layer** before completing the AI and UI layers.

---

# 1. 🎯 Project Goal

CNAS (Criminal Network Analysis System) is designed as an intelligence platform that converts heterogeneous crime/investigation data into a connected and explainable knowledge system.

The core idea is:

```text
Raw Data
   ↓
Data Normalization
   ↓
Entity & Relationship Extraction
   ↓
Entity Resolution
   ↓
Knowledge Graph
   ↓
Graph Intelligence
   ↓
Anomaly Detection
   ↓
Investigation Engine
   ↓
RAG + AI Agent
   ↓
Investigator Dashboard
```

The system should help investigators and analysts discover:

* important entities
* hidden relationships
* communication patterns
* financial relationships
* location relationships
* organizational connections
* communities/groups
* unusual transactions
* unusual network behavior
* relationships between FIRs and entities
* evidence supporting an investigation

---

# 2. ⚠️ Important Principle

CNAS is an **intelligence-support system**, not an automated criminality-detection system.

The system should identify:

> **suspicious, anomalous, or noteworthy patterns**

It should **not automatically conclude that a person is a criminal**.

For example:

```text
❌ "Person X is a criminal."

✅ "Person X is associated with 5 anomalous transactions
   and has a high betweenness score within the observed network."
```

All AI-generated conclusions should be grounded in actual database/document evidence.

---

# 3. 🧠 Core Concept

Traditional systems often store information like:

```text
Person
Phone
Vehicle
Transaction
FIR
Location
```

independently.

CNAS connects them.

Example:

```text
                  Person A
                 /   |    \
                /    |     \
             Phone   Person B  Vehicle
                \      |
                 \   Account
                  \    |
                  Location
                     |
                 Organization
```

The important capability is discovering multi-hop relationships.

For example:

```text
Person A
   ↓
CALLED
   ↓
Person B
   ↓
OWNS
   ↓
Vehicle X
   ↓
VISITED
   ↓
Location Y
```

This allows investigators to explore relationships that may not be obvious from individual records.

---

# 4. 🏗️ System Architecture

Current and planned architecture:

```text
                         ┌───────────────────────┐
                         │      DATA SOURCES     │
                         │                       │
                         │ FIRs / Reports        │
                         │ Transactions          │
                         │ Calls / Emails        │
                         │ Vehicles              │
                         │ Locations             │
                         │ Organizations         │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   DATA INGESTION       │
                         │   Python / FastAPI     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ DATA NORMALIZATION     │
                         │                       │
                         │ Validation             │
                         │ Deduplication          │
                         │ Canonical schemas      │
                         └───────────┬───────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     │                               │
                     ▼                               ▼
             Structured Data                  Unstructured Data
                     │                               │
                     │                         ┌─────▼─────┐
                     │                         │ NLP / LLM │
                     │                         │           │
                     │                         │ NER       │
                     │                         │ Relations │
                     │                         └─────┬─────┘
                     │                               │
                     └───────────────┬───────────────┘
                                     ▼
                         ┌───────────────────────┐
                         │ ENTITY RESOLUTION     │
                         │                       │
                         │ Deduplication         │
                         │ Identity matching     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    KNOWLEDGE GRAPH    │
                         │        Neo4j          │
                         └───────────┬───────────┘
                                     │
                     ┌───────────────┼────────────────┐
                     │               │                │
                     ▼               ▼                ▼
               Graph Analytics   Communities    Anomaly Detection
                     │               │                │
                     └───────────────┼────────────────┘
                                     ▼
                         ┌───────────────────────┐
                         │ INVESTIGATION ENGINE  │
                         └───────────┬───────────┘
                                     │
                     ┌───────────────┼───────────────┐
                     ▼               ▼               ▼
                  Neo4j             RAG             ML
                     │               │               │
                     └───────────────┼───────────────┘
                                     ▼
                         ┌───────────────────────┐
                         │ AI INVESTIGATION      │
                         │ AGENT / LANGGRAPH     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ INVESTIGATOR          │
                         │ DASHBOARD             │
                         └───────────────────────┘
```

---

# 5. 🗺️ Development Roadmap

## M1 — Problem + Architecture ✅

Defined:

* project objective
* data sources
* architecture
* entity model
* relationship model
* technology stack

---

# M2 — Data Inspection + Normalization ✅

Created canonical schemas for:

```text
Person
Phone
Vehicle
Location
Organization
Account
FIR
Relationship
Transaction
```

The normalized data is stored under:

```text
data/processed/
```

---

# M3 — Knowledge Graph ✅

Neo4j is used as the central graph database.

### Main nodes

```text
(:Person)
(:Phone)
(:Vehicle)
(:Location)
(:Organization)
(:Account)
(:FIR)
(:Crime)
(:Event)
(:Transaction)
```

### Main relationships

```text
(:Person)-[:CALLED]->(:Person)

(:Person)-[:EMAILED]->(:Person)

(:Person)-[:USES_PHONE]->(:Phone)

(:Person)-[:OWNS_VEHICLE]->(:Vehicle)

(:Person)-[:VISITED]->(:Location)

(:Person)-[:WORKS_FOR]->(:Organization)

(:Person)-[:HAS_ACCOUNT]->(:Account)

(:Person)-[:INVOLVED_IN]->(:Crime)

(:FIR)-[:MENTIONS]->(:Person)

(:FIR)-[:AT_LOCATION]->(:Location)

(:Person)-[:MADE_TRANSACTION]->(:Transaction)
```

Neo4j `MERGE` and uniqueness constraints should be used to avoid duplicate nodes.

---

# M4 — Graph Intelligence ✅

Current graph analysis includes:

### Degree Centrality

Measures the number of direct connections.

```text
Person A → 47 connections
Person B → 12 connections
```

### Betweenness Centrality

Identifies nodes acting as bridges between parts of the network.

```text
Community A
     |
     |
 Person X
     |
     |
Community B
```

### PageRank

Identifies structurally important nodes.

### Community Detection

Identifies groups/clusters in the network.

Example:

```text
Community 1
 ├── Person A
 ├── Person B
 ├── Phone X
 └── Vehicle Y

Community 2
 ├── Person C
 ├── Person D
 └── Location Z
```

---

# M5 — Anomaly Detection 🚧

The current focus is transaction anomaly detection.

Pipeline:

```text
Transaction
     ↓
Feature Engineering
     ↓
Isolation Forest
     ↓
Anomaly Score
     ↓
Suspicious Activity
```

Current features include:

```text
amount
transaction_frequency
daily_total
unique_accounts
time_of_day
amount_vs_person_average
```

Expected output:

```text
transaction_id
person_id
amount
timestamp
anomaly_score
is_anomaly
reason
```

Example:

```text
Suspicious Transaction

Person: SYN_P_0342

Amount: ₹4,850,000

Anomaly Score: 0.94

Reason:
Transaction amount is unusually high and
occurred during unusual hours.
```

The model should be evaluated against known synthetic anomalies when ground-truth labels are available.

---

# M6 — Investigation Engine ⏳

The investigation engine will provide a unified view of an entity.

Given:

```text
person_id = SYN_P_0342
```

the system should retrieve:

```text
Person
 ├── Phones
 ├── Vehicles
 ├── Organizations
 ├── Accounts
 ├── Locations
 ├── FIRs
 ├── Transactions
 ├── Anomalies
 ├── Connected persons
 └── Communities
```

It should support:

* 1-hop investigation
* 2-hop investigation
* 3-hop investigation
* shortest paths
* common connections
* related entities
* suspicious activity
* graph metrics

---

# M7 — Advanced Graph Intelligence ⏳

Planned capabilities:

* shortest path
* common neighbors
* similarity analysis
* link prediction
* Node2Vec
* graph embeddings
* advanced community analysis
* suspicious subgraph detection

Potential future methods:

```text
Jaccard Similarity
Adamic-Adar
Preferential Attachment
Node2Vec
Graph Embeddings
```

---

# M8 — NLP Entity + Relationship Extraction ⏳

Unstructured documents such as FIRs and reports will be processed.

Example:

```text
"Raj Kumar met Amit Sharma at XYZ Hotel
on 12 August."
```

Expected extraction:

```json
{
  "persons": [
    "Raj Kumar",
    "Amit Sharma"
  ],
  "locations": [
    "XYZ Hotel"
  ],
  "events": [
    {
      "type": "meeting",
      "date": "12 August"
    }
  ]
}
```

Pipeline:

```text
PDF / Document
      ↓
Text Extraction
      ↓
NER
      ↓
Relation Extraction
      ↓
Structured JSON
      ↓
Validation
      ↓
Entity Resolution
      ↓
Neo4j
```

Possible technologies:

* spaCy
* Hugging Face Transformers
* BERT-based NER
* LLM structured extraction
* Pydantic

---

# M9 — RAG + Evidence-Grounded AI Agent ⏳

The AI assistant will combine:

```text
Neo4j
+
Vector Database
+
Documents
+
ML Results
```

Architecture:

```text
                    Investigator
                         │
                         ▼
                Investigation Agent
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Graph Agent    Document Agent   ML Agent
          │              │              │
        Neo4j          Vector DB     Anomaly Model
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                 Evidence Aggregator
                         │
                         ▼
                 Grounded Response
```

Example:

```text
User:

"What connections does SYN_P_0342
have with Organization X?"
```

The agent should:

1. understand the query
2. retrieve graph evidence
3. retrieve relevant documents
4. retrieve anomaly information if relevant
5. combine evidence
6. produce an explanation
7. cite/identify the underlying evidence

The LLM must **not invent relationships**.

---

# M10 — Investigation Timeline ⏳

The system will reconstruct events chronologically.

Example:

```text
2026-01-03
    │
    └── Phone communication

2026-01-08
    │
    └── Vehicle observed at Location X

2026-01-15
    │
    └── Financial transaction

2026-01-17
    │
    └── FIR

2026-01-20
    │
    └── Anomalous transaction
```

This provides temporal context to graph relationships.

---

# M11 — Evidence Integrity 🔜

Planned security/evidence layer:

```text
Document
   ↓
SHA-256
   ↓
Evidence Hash
   ↓
Immutable Audit Record
```

The complete document does not need to be stored on-chain.

Instead:

```text
Actual Evidence
      ↓
Secure Storage

Hash
      ↓
Blockchain / Immutable Ledger
```

This allows the system to verify whether evidence has been modified.

---

# M12 — Backend API ⏳

FastAPI will expose the system.

Planned endpoints:

```text
GET  /api/persons
GET  /api/persons/{id}
GET  /api/persons/{id}/network
GET  /api/persons/{id}/timeline
GET  /api/persons/{id}/anomalies

GET  /api/transactions
GET  /api/anomalies

POST /api/documents
POST /api/investigate
POST /api/search

GET  /api/evidence/{id}
```

---

# M13 — Investigator Dashboard ⏳

The dashboard should provide:

```text
Network Graph
Person Investigation
Timeline
Transaction Analysis
Anomaly Alerts
FIR Search
Community Analysis
AI Investigation Assistant
Evidence
```

Example:

```text
┌─────────────────────────────────────────────┐
│        CNAS INVESTIGATOR DASHBOARD          │
├─────────────────────────────────────────────┤
│ Search: [ SYN_P_0342              ] [Search] │
├─────────────────────────────────────────────┤
│                                             │
│              NETWORK GRAPH                  │
│                                             │
│       Person ─── Phone                      │
│          │       /                          │
│       Vehicle ─ Person ─ Account             │
│          │           │                      │
│       Location       FIR                    │
│                                             │
├─────────────────────────────────────────────┤
│ Degree: 47       PageRank: 0.018             │
│ Community: 3     Anomalies: 4                │
├─────────────────────────────────────────────┤
│ Timeline                                    │
│ ● Call                                      │
│ ● Location                                  │
│ ● Transaction                               │
│ ● FIR                                       │
└─────────────────────────────────────────────┘
```

---

📁 Project Structure
CNAS/
│
├── agents/                         # Agent-related components / experiments
│
├── backend/                        # Backend application layer
│   └── app/
│       ├── api/                    # API routes
│       │   ├── network.py
│       │   ├── persons.py
│       │   └── router.py
│       │
│       ├── core/                   # Backend configuration/database
│       │   └── database.py
│       │
│       ├── services/               # Backend business services
│       │   ├── network_service.py
│       │   └── person_service.py
│       │
│       └── main.py                 # Backend application entry point
│
├── data/                           # All project datasets
│   │
│   ├── raw/                        # Original/raw datasets
│   │   └── CNAS_Prototype_Data/
│   │
│   ├── processed/                  # Normalized datasets used by CNAS
│   │   ├── persons.csv
│   │   ├── phones.csv
│   │   ├── vehicles.csv
│   │   ├── locations.csv
│   │   ├── organizations.csv
│   │   ├── accounts.csv
│   │   ├── firs.csv
│   │   ├── relationships.csv
│   │   ├── relationships_calls.csv
│   │   ├── relationships_emails.csv
│   │   ├── relationships_transactions.csv
│   │   ├── relationships_visits.csv
│   │   ├── relationships_works_for.csv
│   │   └── anomaly_alerts.csv
│   │
│   ├── documents/                  # FIRs and unstructured documents
│   │   ├── raw/
│   │   ├── processed/
│   │   └── real_firs/
│   │
│   ├── reports/                    # Dataset profiling/inventory reports
│   │   ├── data_inventory.json
│   │   └── dataset_summary.csv
│   │
│   └── synthetic/                  # Generated/synthetic datasets
│
├── models/                         # Trained ML/graph models
│   └── node2vec.model
│
├── scripts/                        # Utility, pipeline and validation scripts
│   ├── inventory.py
│   ├── run_pipeline.py
│   ├── run_m8_pipeline.py
│   ├── combine_relationships.py
│   │
│   ├── normalize_*.py              # Data normalization scripts
│   │
│   └── test_*.py                   # Component/integration tests
│
├── src/                            # Core CNAS intelligence platform
│   │
│   ├── ingestion/                  # Data ingestion pipelines
│   │
│   ├── preprocessing/              # Data cleaning/preprocessing
│   │
│   ├── entity_resolution/          # Entity matching/deduplication
│   │
│   ├── extraction/                 # Information extraction
│   │
│   ├── nlp/                        # NLP and entity/relation extraction
│   │   ├── entity_extractor.py
│   │   ├── ner.py
│   │   ├── text_loader.py
│   │   ├── text_extractor.py
│   │   ├── normalizer.py
│   │   ├── validator.py
│   │   ├── schemas.py
│   │   ├── pipeline.py
│   │   └── neo4j_writer.py
│   │
│   ├── graph/                      # Neo4j Knowledge Graph
│   │   ├── neo4j_client.py
│   │   ├── create_constraints.py
│   │   ├── load_nodes.py
│   │   ├── load_relationships.py
│   │   ├── load_fir_graph.py
│   │   ├── graph_queries.py
│   │   ├── graph_intelligence.py
│   │   ├── investigation_service.py
│   │   └── validate_graph.py
│   │
│   ├── intelligence/               # Network/graph intelligence
│   │   ├── graph_loader.py
│   │   ├── centrality.py
│   │   ├── communities.py
│   │   ├── network_analysis.py
│   │   ├── analyze_person.py
│   │   └── run_analysis.py
│   │
│   ├── anomaly/                    # Suspicious/anomalous activity detection
│   │   ├── feature_engineering.py
│   │   ├── features.py
│   │   ├── isolation_forest.py
│   │   ├── detector.py
│   │   ├── anomaly_reasons.py
│   │   ├── evaluate_model.py
│   │   └── run_anomaly_detection.py
│   │
│   ├── investigation/              # Investigation intelligence engine
│   │   ├── investigation_engine.py
│   │   ├── investigation_queries.py
│   │   ├── investigation_indicators.py
│   │   ├── link_prediction.py
│   │   ├── hybrid_link_prediction.py
│   │   ├── node2vec.py
│   │   └── run_investigation.py
│   │
│   ├── agent/                      # AI investigation agents
│   │   ├── investigation_agent.py
│   │   ├── anomaly_agent.py
│   │   ├── entity_extractor.py
│   │   ├── graph.py
│   │   ├── graph_tools.py
│   │   ├── rag_tools.py
│   │   ├── evidence.py
│   │   └── state.py
│   │
│   ├── rag/                        # Retrieval-Augmented Generation
│   │   ├── document_loader.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── answer_generator.py
│   │   └── rag_pipeline.py
│   │
│   ├── api/                        # FastAPI application
│   │   ├── main.py
│   │   ├── dependencies.py
│   │   ├── routes/
│   │   │   ├── persons.py
│   │   │   ├── network.py
│   │   │   ├── graph.py
│   │   │   ├── anomalies.py
│   │   │   ├── investigation.py
│   │   │   ├── documents.py
│   │   │   ├── evidence.py
│   │   │   ├── transactions.py
│   │   │   ├── agents.py
│   │   │   └── search.py
│   │   │
│   │   ├── schemas/                # API request/response models
│   │   └── services/               # API business logic
│   │
│   ├── communities/                # Community detection components
│   ├── link_prediction/            # Link prediction components
│   ├── risk/                       # Risk scoring
│   └── config.py                   # Global configuration
│
├── frontend/                       # Investigator dashboard
│   │
│   ├── src/
│   │   ├── api/                    # Backend API clients
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── dashboard/
│   │   │   ├── layout/
│   │   │   ├── network/
│   │   │   └── person/
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Persons.tsx
│   │   │   ├── PersonInvestigation.tsx
│   │   │   ├── NetworkExplorer.tsx
│   │   │   ├── Anomalies.tsx
│   │   │   ├── Transactions.tsx
│   │   │   ├── Documents.tsx
│   │   │   ├── Cases.tsx
│   │   │   └── Investigation.tsx
│   │   │
│   │   └── App.tsx
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── security/                       # Security, authentication and audit components
│
├── tests/                          # Project-wide tests
│
├── notebook/                       # Research/experimentation notebooks
│
├── docker-compose.yaml             # Local infrastructure
├── pyproject.toml                  # Python project configuration
├── requirements.txt                # Python dependencies
├── uv.lock                         # Locked Python dependencies
├── package-lock.json               # Node dependencies
└── README.md                       # Project documentation

> The structure can evolve as the project grows. Do not create empty modules simply to match the roadmap; add them when their corresponding milestone is implemented.


---

🏗️ Architecture Overview

CNAS follows a layered architecture:

                        ┌─────────────────────────┐
                        │      Investigator       │
                        │       Dashboard         │
                        │    React + TypeScript    │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │       FastAPI           │
                        │       REST APIs         │
                        └────────────┬────────────┘
                                     │
                 ┌───────────────────┼───────────────────┐
                 │                   │                   │
                 ▼                   ▼                   ▼
        ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
        │ Investigation  │  │  AI Agents     │  │  Anomaly       │
        │ Engine         │  │  + RAG         │  │  Detection     │
        └───────┬────────┘  └───────┬────────┘  └───────┬────────┘
                │                   │                   │
                └───────────────────┼───────────────────┘
                                    ▼
                         ┌────────────────────┐
                         │  Graph Intelligence│
                         │ NetworkX / Neo4j   │
                         └──────────┬─────────┘
                                    │
                                    ▼
                         ┌────────────────────┐
                         │   Neo4j Knowledge  │
                         │       Graph        │
                         └──────────┬─────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
           ┌─────────────────┐             ┌─────────────────┐
           │ Structured Data │             │ Documents / FIRs│
           │ CSV / JSON      │             │ PDF / TXT       │
           └────────┬────────┘             └────────┬────────┘
                    │                               │
                    ▼                               ▼
           ┌─────────────────┐             ┌─────────────────┐
           │ Data Processing │             │ NLP / Extraction│
           │ + Normalization │             │ NER + Relations │
           └─────────────────┘             └─────────────────┘

# 7. 🗃️ Data Model

## Person

```text
person_id
name
gender
age
source
confidence
```

## Phone

```text
phone_id
phone_number
source
```

## Vehicle

```text
vehicle_id
registration_number
vehicle_type
source
```

## Location

```text
location_id
name
latitude
longitude
source
```

## Organization

```text
organization_id
name
type
source
```

## Account

```text
account_id
bank
account_type
source
```

## FIR

```text
fir_id
date
police_station
crime_type
description
source
```

## Relationship

The relationship table is central to the graph:

```text
relationship_id
source_id
source_type
relationship
target_id
target_type
timestamp
source_document
confidence
provenance
```

---

# 8. 🔗 Graph Design

Examples:

```text
(Person)-[:CALLED]->(Person)

(Person)-[:USES_PHONE]->(Phone)

(Person)-[:OWNS_VEHICLE]->(Vehicle)

(Person)-[:VISITED]->(Location)

(Person)-[:WORKS_FOR]->(Organization)

(Person)-[:HAS_ACCOUNT]->(Account)

(Person)-[:INVOLVED_IN]->(Crime)

(FIR)-[:MENTIONS]->(Person)

(FIR)-[:AT_LOCATION]->(Location)

(Person)-[:MADE_TRANSACTION]->(Transaction)
```

When adding new relationships, document:

```text
relationship name
source node
target node
meaning
required properties
data source
confidence/provenance
```

---

# 9. 🛠️ Technology Stack

| Layer               | Technology                            |
| ------------------- | ------------------------------------- |
| Programming         | Python                                |
| Data Processing     | Pandas, NumPy                         |
| ML                  | Scikit-learn                          |
| Graph Database      | Neo4j                                 |
| Graph Analysis      | NetworkX / Neo4j algorithms           |
| NLP                 | spaCy / Hugging Face                  |
| LLM                 | Gemini / OpenAI                       |
| RAG                 | LangChain                             |
| Agents              | LangGraph                             |
| Backend             | FastAPI                               |
| Frontend            | React / Streamlit                     |
| Vector Database     | FAISS / Chroma                        |
| Database            | PostgreSQL                            |
| Cache               | Redis                                 |
| Containers          | Docker                                |
| Experiment Tracking | MLflow                                |
| Data Versioning     | DVC                                   |
| CI/CD               | GitHub Actions                        |
| Security            | JWT + RBAC                            |
| Evidence Integrity  | SHA-256 + blockchain/immutable ledger |

Not every technology is required immediately. Prefer a working simple implementation over adding unnecessary infrastructure.

---

# 10. 💻 Local Development Setup

## Prerequisites

Install:

* Python 3.10+
* Git
* Docker
* Docker Compose
* Neo4j
* `uv` recommended

Verify:

```bash
python --version
git --version
docker --version
```

If using `uv`:

```bash
uv --version
```

---

# 11. 📥 Clone the Repository

```bash
git clone <REPOSITORY_URL>
cd CNAS
```

Replace `<REPOSITORY_URL>` with the team's GitHub repository URL.

---

# 12. 🐍 Create the Python Environment

Recommended:

```bash
uv sync
```

If dependencies have not yet been defined:

```bash
uv add pandas numpy scikit-learn neo4j python-dotenv
```

Activate the environment if needed:

```bash
source .venv/bin/activate
```

---

# 13. 🔐 Configure Environment Variables

Create:

```text
.env
```

Example:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

# LLM configuration
GOOGLE_API_KEY=your_api_key

# Optional future services
OPENAI_API_KEY=your_api_key
```

### IMPORTANT

Never commit `.env`.

The repository should contain:

```text
.env.example
```

Example:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=

GOOGLE_API_KEY=
OPENAI_API_KEY=
```

Each developer creates their own `.env`.

---

# 14. 🐳 Start Neo4j

If the project already contains Docker Compose:

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

Neo4j Browser is normally available at:

```text
http://localhost:7474
```

Bolt connection:

```text
bolt://localhost:7687
```

Use the username/password configured in `.env`.

---

# 15. 📊 Prepare the Data

Place raw datasets in:

```text
data/raw/
```

Normalized datasets should be placed in:

```text
data/processed/
```

Do not modify raw data directly.

Recommended pipeline:

```text
data/raw/
    ↓
validation
    ↓
normalization
    ↓
data/processed/
```

---

# 16. 🔍 Validate Data

Before loading into Neo4j:

```bash
python -m src.anomaly.load_transactions
```

or, when available, run the project's data validation scripts.

Check:

```text
columns
row counts
missing values
duplicate IDs
invalid relationships
```

---

# 17. 🕸️ Load Knowledge Graph

Create constraints:

```bash
python -m src.graph.create_constraints
```

Load nodes:

```bash
python -m src.graph.load_nodes
```

Load relationships:

```bash
python -m src.graph.load_relationships
```

If FIR-specific loaders are available:

```bash
python -m src.graph.load_fir_graph
```

Validate:

```bash
python -m src.graph.validate_graph
```

---

# 18. 📈 Run Graph Intelligence

Run the graph analysis pipeline:

```bash
python -m src.intelligence.run_analysis
```

The system should calculate metrics such as:

```text
degree
betweenness
pagerank
community
```

---

# 19. 🚨 Run Anomaly Detection

Run:

```bash
python -m src.anomaly.run_anomaly_detection
```

Expected output:

```text
Total transactions : XXXX

Anomalies detected  : XXX

Normal transactions: XXXX

Anomaly percentage  : XX.XX%
```

Output should be generated under:

```text
data/processed/
```

For example:

```text
transaction_anomalies.csv
anomaly_alerts.csv
```

---

# 20. 🔎 Verify the Graph

Open Neo4j Browser and run:

```cypher
MATCH (n)
RETURN n
LIMIT 100;
```

Check relationship types:

```cypher
MATCH ()-[r]->()
RETURN type(r), count(r)
ORDER BY count(r) DESC;
```

Check Person relationships:

```cypher
MATCH path =
    (p:Person)-[r]-(x)
RETURN path
LIMIT 50;
```

Check suspicious transactions:

```cypher
MATCH (p:Person)-[:MADE_TRANSACTION]->(t:Transaction)
WHERE t.is_anomaly = true
RETURN p, t
LIMIT 30;
```

---

# 21. 🔬 Useful Investigation Queries

### Person network

```cypher
MATCH path =
    (p:Person)-[*1..3]-(x)
WHERE p.person_id = $person_id
RETURN path;
```

### Direct connections

```cypher
MATCH (p:Person)-[r]-(x)
WHERE p.person_id = $person_id
RETURN type(r), labels(x), x;
```

### Highly connected people

```cypher
MATCH (p:Person)
OPTIONAL MATCH (p)--(x)
RETURN
    p.person_id,
    count(DISTINCT x) AS degree
ORDER BY degree DESC
LIMIT 20;
```

### Suspicious transactions

```cypher
MATCH (p:Person)-[:MADE_TRANSACTION]->(t:Transaction)
WHERE t.is_anomaly = true
RETURN
    p.person_id,
    t.transaction_id,
    t.amount,
    t.anomaly_score,
    t.reason
ORDER BY t.anomaly_score DESC
LIMIT 20;
```

---

# 22. 🧪 Testing Philosophy

Every new module should have tests.

Recommended:

```text
tests/
├── test_data_validation.py
├── test_graph.py
├── test_graph_queries.py
├── test_anomaly_detection.py
├── test_nlp_extraction.py
├── test_entity_resolution.py
└── test_api.py
```

At minimum, test:

```text
Input validation
Expected output
Empty data
Missing values
Duplicate IDs
Invalid relationships
Model execution
Neo4j connectivity
```

---

# 23. 📏 Reliability & Evaluation

A successful run is not enough.

CNAS should eventually measure:

## Data quality

```text
Missing values
Duplicate entities
Invalid IDs
Invalid relationships
Orphan nodes
```

## Anomaly detection

If known anomaly labels exist:

```text
Precision
Recall
F1-score
ROC-AUC
PR-AUC
```

## NLP

```text
Entity precision
Entity recall
Entity F1
Relation precision
Relation recall
Relation F1
```

## Graph

```text
Number of nodes
Number of relationships
Connected components
Duplicate nodes
Orphan nodes
```

## AI Agent

Measure:

```text
Answer correctness
Evidence grounding
Hallucination rate
Graph-query success rate
```

---

# 24. 🤝 Collaboration Guidelines

This repository is intended for collaborative development.

## Branch strategy

Do not directly push experimental work to `main`.

Use:

```text
main
 │
 ├── feature/anomaly-improvements
 ├── feature/investigation-engine
 ├── feature/nlp-extraction
 ├── feature/rag-agent
 ├── feature/dashboard
 └── fix/neo4j-loader
```

Example:

```bash
git checkout -b feature/investigation-engine
```

---

# 25. 🔄 Development Workflow

Recommended workflow:

```text
1. Pull latest main
        ↓
2. Create feature branch
        ↓
3. Implement feature
        ↓
4. Test locally
        ↓
5. Update documentation
        ↓
6. Commit
        ↓
7. Push branch
        ↓
8. Open Pull Request
        ↓
9. Code review
        ↓
10. Merge
```

Commands:

```bash
git checkout main
git pull origin main

git checkout -b feature/<feature-name>

git add .
git commit -m "feat: add <feature>"

git push origin feature/<feature-name>
```

---

# 26. 📝 Commit Convention

Use meaningful commit messages.

Examples:

```text
feat: add transaction anomaly detection
feat: add person investigation endpoint
feat: add FIR entity extraction

fix: resolve Neo4j relationship loading issue
fix: handle missing transaction timestamps

refactor: improve graph loader

test: add anomaly detection tests

docs: update project architecture
```

Avoid:

```text
update
changes
final
new code
working
test
```

---

# 27. 🔐 Security Rules

Never commit:

```text
.env
API keys
passwords
private certificates
database credentials
tokens
```

Make sure `.gitignore` contains:

```text
.env
.venv/
__pycache__/
*.pyc
*.log
.ipynb_checkpoints/
```

If credentials are accidentally committed, rotate them immediately.

---

# 28. 📌 Evidence & Provenance

Every extracted intelligence record should ideally preserve:

```text
source
source_document
timestamp
confidence
provenance
```

Example:

```json
{
  "person_id": "SYN_P_0342",
  "relationship": "CALLED",
  "target_id": "SYN_P_0102",
  "source_document": "FIR_102.pdf",
  "confidence": 0.93,
  "provenance": "FIR_102.pdf:page_3"
}
```

This becomes critical for the future AI investigation system.

---

# 29. 🧠 AI Grounding Rules

When the AI agent is implemented:

### Rule 1

Neo4j is the source of truth for graph relationships.

### Rule 2

The vector database is the source for retrieved document context.

### Rule 3

ML models provide analytical signals.

### Rule 4

The LLM explains retrieved evidence.

### Rule 5

The LLM should never invent relationships.

### Rule 6

Every important claim should be traceable to evidence.

Bad:

```text
"Person A is definitely part of Organization X."
```

Good:

```text
"Person A is connected to Organization X through
the WORKS_FOR relationship recorded in source document X."
```

---

# 30. 🚀 Future Production Architecture

Eventually:

```text
                    ┌─────────────────────┐
                    │ Investigator UI     │
                    │ React               │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ FastAPI Gateway     │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
      Investigation       AI Agent           Analytics
         Engine            LangGraph           Engine
             │                 │                  │
             ▼          ┌──────┼──────┐           ▼
           Neo4j         │      │      │       ML Models
                         ▼      ▼      ▼
                       RAG    Neo4j   Tools
                         │
                         ▼
                    Vector DB
```

Supporting infrastructure:

```text
PostgreSQL
Redis
Docker
MLflow
DVC
GitHub Actions
AWS
```

---

# 31. 🏆 Final Demonstration Flow

The final CNAS demonstration should ideally work like this:

```text
Investigator
      │
      ▼
Search Person
      │
      ▼
Person Investigation
      │
      ├───────────────┐
      ▼               ▼
Knowledge Graph     Timeline
      │               │
      ▼               ▼
Relationships      Events
      │
      ▼
Graph Analytics
      │
      ├── Degree
      ├── Betweenness
      ├── PageRank
      └── Community
      │
      ▼
Transaction Analysis
      │
      ▼
Anomaly Detection
      │
      ▼
Evidence Retrieval
      │
      ▼
AI Investigation Agent
      │
      ▼
Evidence-Grounded Answer
```

Example final interaction:

```text
Investigator:

"Investigate SYN_P_0342."
```

CNAS:

```text
Person: SYN_P_0342

Network:
47 direct connections

Graph:
Betweenness: 0.72
PageRank: 0.018
Community: 3

Transactions:
5 anomalous transactions

Connected:
3 phones
2 vehicles
7 locations
2 organizations

FIR:
3 related FIR records

Evidence:
FIR-102, Transaction-TX3942, Call-CDR-821
```

The investigator can then ask:

```text
"Why is this person important?"
```

and receive an explanation based only on retrieved evidence.

---

# 32. 👥 Suggested Team Responsibilities

For a team, divide work by system components.

### Member 1 — Data Engineering

Responsible for:

```text
Data ingestion
Normalization
Validation
Entity resolution
Data quality
```

### Member 2 — Graph Engineering

Responsible for:

```text
Neo4j
Graph schema
Loaders
Cypher
Graph algorithms
```

### Member 3 — ML / Anomaly Detection

Responsible for:

```text
Feature engineering
Isolation Forest
Anomaly detection
Model evaluation
Graph anomaly detection
```

### Member 4 — NLP / GenAI

Responsible for:

```text
NER
Relation extraction
RAG
LangGraph
Investigation Agent
```

### Member 5 — Backend / Frontend

Responsible for:

```text
FastAPI
React/Streamlit
Graph visualization
Dashboard
Authentication
```

Responsibilities can overlap. All contributors should review each other's changes.

---

# 33. 🧩 Current Priority

The immediate priority should **not** be adding random technologies.

Follow this order:

```text
M5
Anomaly Detection
       ↓
M6
Investigation Engine
       ↓
M7
Advanced Graph Intelligence
       ↓
M8
NLP Entity/Relation Extraction
       ↓
M9
RAG + AI Investigation Agent
       ↓
M10
Investigation Timeline
       ↓
M12
FastAPI
       ↓
M13
Investigator Dashboard
       ↓
Security + Evaluation + Deployment
```

The project should first have a reliable intelligence backend, then expose it through AI and UI.

---

# 34. 🎯 Definition of Done

CNAS should be considered a strong prototype when an investigator can:

```text
[✓] Search for a person

[✓] View their connected entities

[✓] Explore 1–3 hop relationships

[✓] See graph importance metrics

[✓] Identify their community

[✓] View associated transactions

[✓] Detect anomalous transactions

[✓] View related FIRs

[✓] See investigation events chronologically

[✓] Upload/search documents

[✓] Extract entities from documents

[✓] Ask an AI investigation question

[✓] Receive evidence-grounded results

[✓] Trace results back to source evidence

[✓] Verify evidence integrity

[✓] Control access through user roles

[✓] Run the complete system locally with documented steps
```

---

# 35. 📣 Project Vision

CNAS aims to move from:

```text
Disconnected crime records
```

to:

```text
Connected intelligence
```

and ultimately:

```text
Data
 ↓
Knowledge
 ↓
Relationships
 ↓
Patterns
 ↓
Anomalies
 ↓
Evidence
 ↓
Investigation
```

The long-term goal is to build an **evidence-grounded graph intelligence platform** where graph analytics, machine learning, NLP, and AI agents work together to help investigators understand complex networks while keeping the underlying evidence and provenance visible.

---

## 🤝 Contributing

Contributions are welcome.

Before contributing:

1. Create an issue describing the feature/bug.
2. Create a feature branch.
3. Implement and test the change.
4. Update documentation if necessary.
5. Open a Pull Request.
6. Wait for review before merging.

Please keep changes modular and avoid committing secrets or raw sensitive data.

---

## 📄 License

Add the project's chosen license here.

Example:

```text
MIT License
```

---

## 👨‍💻 Project Team

**CNAS — Criminal Network Analysis System**

Built as an AI + Knowledge Graph + Network Intelligence project.

### Core technologies

```text
Python
Neo4j
NetworkX
Scikit-learn
FastAPI
LangChain
LangGraph
Hugging Face
Docker
MLflow
DVC
```

---

## ⭐ Project Principle

> **Connect the evidence. Analyze the network. Detect the anomaly. Explain the evidence.**

**CNAS is designed to assist human investigation—not replace human judgment.**


## Quick start

1. Create a Python environment and install dependencies.
2. Configure environment variables in `.env`.
3. Start the API:

   uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

4. Start the frontend:

   cd frontend && npm install && npm run dev

## Required environment variables

- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `PINECONE_API_KEY`
- `GOOGLE_API_KEY`
- `ALLOWED_ORIGINS`

## Health check

- `GET /health`

## Architecture

- FastAPI API backend
- Neo4j graph database
- Pinecone vector index
- React + Vite frontend
- GraphRAG investigation flow
