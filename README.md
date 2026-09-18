# 🔐 Secure Enterprise AI Research Agent

An authorization-aware AI research assistant designed to answer employee questions using enterprise documents while preventing unauthorized information from reaching the AI model.

## 🎯 Problem

Enterprise organizations store information with different security classifications such as:

* Public
* Internal
* Confidential
* Restricted

Employees have different roles, departments, and permissions.

A normal RAG system may retrieve relevant documents and send them directly to an LLM. This creates a security risk if the retrieved documents contain information the employee is not authorized to access.

This project addresses that problem by enforcing authorization **before document content reaches the LLM**.

## 💡 Solution

The system follows this security pipeline:

```text
Employee Question
       ↓
User Context
       ↓
Document Retrieval
       ↓
Authorization Filter
       ↓
Authorized Evidence Only
       ↓
Version / Conflict Handling
       ↓
LLM
       ↓
Answer + Sources
       ↓
Audit Log
```

The key security principle is:

> **Unauthorized document content must never be provided to the LLM.**

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │    Streamlit UI  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Research Agent   │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │    Retrieval      │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Authorization     │
                    │     Filter        │
                    └────────┬─────────┘
                             │
                    Authorized Documents
                             │
                    ┌────────▼─────────┐
                    │ Version Handling  │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │   LLM / Answer    │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │   Audit Logging   │
                    └──────────────────┘
```

## 🔐 Security Model

The system uses user information including:

* User ID
* Department
* Role
* Clearance

Documents contain access metadata including:

* Document ID
* Classification
* Allowed departments
* Allowed roles
* Version
* Effective date
* Content

Authorization is performed before evidence is prepared for the LLM.

If no accessible evidence exists, the system returns:

```text
No accessible information was found for this question.
```

The inaccessible document content is not passed to the LLM.

## 🧠 Main Components

### `auth/`

Handles user and document authorization.

### `rag/`

Retrieves documents that are relevant to the user's question while respecting authorization.

### `agent/`

Coordinates retrieval, version selection, evidence preparation, and answer generation.

### `services/`

Contains supporting services such as:

* Version handling
* LLM interaction
* Audit logging

### `tests/`

Contains automated tests for:

* Authorization
* Retrieval
* Version selection
* Security
* LLM evidence handling

### `data/`

Contains the prototype user and document metadata.

## 🧪 Test Scenarios

### Test A — Authorized Finance User

**User:** U102
**Question:** What is the Q4 revenue forecast?

Expected result:

```text
Q4 projected revenue is 120 crore.
Source: DOC-101
Version: 2.0
```

### Test B — Unauthorized Marketing User

**User:** U205
**Question:** What is the Q4 revenue forecast?

The restricted executive document contains a different forecast, but U205 is not authorized to access it.

Expected result:

```text
No accessible information was found for this question.
```

The restricted value must not be exposed.

### Test C — Latest Authorized Version

**User:** U301
**Question:** What is the Q4 forecast?

The system has two authorized versions:

```text
DOC-301 → v1.0 → 110 crore
DOC-302 → v2.0 → 125 crore
```

Expected result:

```text
Q4 projected revenue is 125 crore.
Source: DOC-302
Version: 2.0
```

## 📊 Audit Logging

Each research request can be recorded with information such as:

* Timestamp
* User ID
* Query
* Status
* Authorization decision
* Evidence document IDs
* Sources

The audit log is designed to record security-relevant metadata without storing unauthorized document content.

## 🛠️ Tech Stack

* Python
* Streamlit
* Pytest
* JSON-based prototype data
* Git / GitHub
* OpenAI API integration
* Retrieval and authorization pipeline

## 🚀 Running the Project

Clone the repository and enter the project directory.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
python -m pytest
```

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The application will be available locally through the Streamlit local URL.

## 📁 Project Structure

```text
secure-enterprise-ai-research-agent/
│
├── agent/
│   └── research_agent.py
│
├── auth/
│   └── authorization.py
│
├── data/
│   ├── users.json
│   ├── documents.json
│   └── audit_log.json
│
├── docs/
│
├── rag/
│   └── retrieval.py
│
├── services/
│   ├── audit.py
│   ├── llm.py
│   └── versioning.py
│
├── tests/
│   ├── test_authorization.py
│   ├── test_retrieval.py
│   ├── test_versions.py
│   ├── test_security.py
│   └── test_llm.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🔭 Future Scope

Possible improvements include:

* Production-grade authentication
* Database-backed document storage
* Vector database retrieval
* More granular permissions
* Document ownership rules
* Stronger classification and clearance enforcement
* Improved conflict detection
* Enterprise identity-provider integration
* More detailed audit dashboards
* Automated CI/CD testing

## ⚠️ Prototype Note

This project is a hackathon prototype demonstrating the authorization-aware research workflow.

The current implementation uses sample users and documents to demonstrate the security architecture and test scenarios.

Production deployment would require additional security controls, enterprise authentication, persistent storage, stronger access policies, and security review.

## 👥 Team

Built as a hackathon project by our team.

---

**Core principle:**

### 🔒 Search widely, authorize strictly, and send only authorized evidence to the AI.
## Demo Scenarios

### Test A — Authorized User

User: U102  
Department: Finance  
Clearance: Internal

Question:

> What is the Q4 revenue forecast?

Expected result:

- Answer: 120 crore
- Source: DOC-101
- Authorization: ALLOWED
- LLM Evidence: DOC-101

### Test B — Unauthorized User

User: U205  
Department: Marketing  
Clearance: Internal

Question:

> What is the Q4 revenue forecast?

Expected result:

- Access: DENIED
- LLM Evidence: None
- Restricted value from DOC-201 must not be disclosed

### Test C — Latest Authorized Version

User: U301  
Department: Finance  
Clearance: Internal

Question:

> What is the Q4 forecast?

Expected result:

- Latest authorized document: DOC-302
- Version: 2.0
- Answer: 125 crore

## Security Guarantee

The system follows this order:

User Request
→ Document Retrieval
→ Authorization Check
→ Version Selection
→ Authorized Evidence
→ LLM
→ Answer

Unauthorized document content is removed before the LLM receives evidence.

## Testing

Run:

```powershell
python -m pytest -v