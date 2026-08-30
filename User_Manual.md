# ShadowNet User Manual

Welcome to **ShadowNet Intelligence**, an evidence-grounded criminal intelligence and network analysis platform. This guide will walk you through how to use the website to investigate entities, explore networks, and uncover anomalous activities.

---

## 1. Getting Started: The Dashboard
When you log in, you are greeted by the **Dashboard**. 
* **Purpose**: This is your command center. It provides a high-level summary of the system's current state.
* **How to use**: Review the statistics cards at the top (e.g., total persons, relationships, active cases). Check the recent alerts panel to quickly jump into high-priority anomalous transactions or newly uploaded documents.

---

## 2. Finding Subjects: The Persons Directory
The **Persons** page is your starting point for individual investigations.
* **Purpose**: A comprehensive, searchable database of all individuals known to the system.
* **How to use**: 
  1. Navigate to the **Persons** tab in the sidebar.
  2. Use the search bar to look up a suspect by name, ID, or phone number.
  3. Filter the list based on risk scores or community involvement.
  4. Click on a person's name to open their **Person Investigation** profile.

---

## 3. Deep Dive: Person Investigation Profile
Once you click on an entity, you enter the **Person Investigation** view. This provides a 360-degree look at the individual.
* **Key Features**:
  * **Graph Metrics**: View their central importance to the network (e.g., Degree Centrality, Betweenness). High betweenness means this person acts as a bridge between different criminal groups.
  * **Ego-Network Graph**: A visual web showing this person's immediate connections (1-hop or 2-hop radius) to vehicles, phones, accounts, and other people.
  * **Event Timeline**: A chronological list of all known events involving this person (e.g., a phone call on Monday, a suspicious transaction on Wednesday, an FIR mention on Friday).
* **How to use**: Use the visual graph to spot shared assets (like a shared vehicle or bank account) with other known entities. Use the timeline to reconstruct their movements and actions leading up to a crime.

---

## 4. Seeing the Big Picture: Network Explorer
The **Network Explorer** provides a bird's-eye view of the entire ShadowNet knowledge graph.
* **Purpose**: To identify structural patterns, large syndicates, and isolated communities that you wouldn't see by looking at a single person.
* **How to use**: 
  1. Open the **Network Explorer** from the sidebar.
  2. The graph will populate with nodes (entities) and edges (relationships).
  3. **Pan and Zoom** using your mouse to navigate the canvas.
  4. **Click a node** to expand its connections or view its properties in the side panel.

---

## 5. Following the Money: Transactions & Anomalies
Financial intelligence is split into two primary views:
* **Transactions Page**: A raw ledger view. Use this to manually search for specific bank accounts, filter by date ranges, and trace the flow of funds.
* **Anomalies Page**: The system's Machine Learning alerts. 
  * **How to use**: Review the list of transactions flagged by the AI. Click on an anomaly to see the **Anomaly Score** and the plain-text reasoning (e.g., "Transaction amount is unusually high and occurred at 3:00 AM").

---

## 6. Document Processing
The **Documents** page allows you to ingest raw data.
* **Purpose**: Uploading unstructured text like FIRs, PDFs, and field reports.
* **How to use**: Upload a document. The system's NLP pipeline will automatically read the text, extract names, locations, and relationships, and fuse them into the Knowledge Graph for future investigations.

---

## 7. The AI Investigation Assistant
Stuck on a case? Use the **Investigation** chat interface.
* **Purpose**: A natural language assistant that understands the graph and all uploaded documents.
* **How to use**: 
  1. Type a question like: *"How is Person X connected to Organization Y?"* or *"What evidence do we have against Person Z?"*
  2. The AI agent will traverse the graph, read relevant documents, and provide a plain-English answer.
  3. **Important**: The AI will always provide citations mapping back to the original database entry or FIR document. Always verify the citations!

---

### ⚠️ Important Reminder for Investigators
ShadowNet is an **intelligence-support system**. It identifies suspicious, anomalous, or noteworthy patterns to assist you. It does *not* automatically conclude that a person is guilty. Always ground your final conclusions in the cited evidence and official reports.
