# The Employee Who Asked for Too Much

## 1. Team Details

**Team Name / ID:** Fast & Curious

**Team Lead:** GURRAM INDUPRIYA

**Team Members:**

* KONDURI SRI HARSHITHA
* KANDLAKUTI DIVYA
* REBBA JAHNAVI
* ABBAGOUNI RISHITHA

**Repo Link (Optional):** https://github.com/rebbajahnavi/secure-enterprise-ai-research-agent

**Demo Link (Optional):** https://secure-enterprise-ai-research-agent-fastandcurious.streamlit.app/

---

## 2. Problem Statement

# The Employee Who Asked for Too Much

## Context

Your company has thousands of internal documents. Employees can ask questions such as:

**"What was the revenue forecast for Q4?"**

An AI assistant should be able to search documents, understand them, compare information and answer questions. But not every employee is allowed to access every document. Documents have classifications:

* Public
* Internal
* Confidential
* Restricted

Different employees have different permissions. The assistant must answer a question **without exposing information that the employee is not authorized to access**.

Documents may also:

* contradict each other
* be outdated
* have different versions
* contain incomplete information

**Critical requirement**

An unauthorized document must **never be provided to the LLM simply because it is relevant to the question**.

## The Challenge

Build a secure enterprise research agent that answers employee questions over internal documents while enforcing authorization. Documents have classifications and access rules. Relevant information that the requesting employee is not authorized to access must never be provided to the language model or revealed in the final answer.

## Core Requirements

* Accept a natural-language employee question and user context.
* Ingest documents with classification, department, owner, and access-control metadata.
* Search for relevant candidates but enforce authorization before document content reaches the LLM.
* Handle outdated and conflicting authorized documents.
* Return an answer with citations to the evidence the user is allowed to access.
* Record an audit trail of the request, authorization decisions, and evidence used.
* Safely respond when the answer exists only in documents the user cannot access.

---

## 3. TL;DR

**Problem:** AI assistants can leak sensitive enterprise data when retrieval ignores employee access permissions.

**Solution:** Our secure research agent applies authorization before LLM processing, filters evidence by access level, resolves document versions, provides citations, and records audit information.

**Who benefits:** Enterprise employees receive trustworthy answers while organizations reduce the risk of unauthorized data exposure and improve auditability.

---

## 4. Scope of the Project

**What are you building?**

A secure enterprise research agent that accepts employee questions, searches internal documents, enforces authorization before LLM processing, selects the latest authorized evidence, provides citations, and records security decisions.

**How does it solve the problem statement?**

The system separates retrieval from authorization. Relevant documents are filtered according to user permissions before their content can become LLM evidence. If no authorized evidence exists, the system refuses to provide the protected information.

**Key features you're building for this hackathon:**

* **Pre-LLM Authorization Firewall** — prevents unauthorized document content from reaching the LLM.
* **Role-Based Access Control** — applies security levels and role permissions to retrieval.
* **Version & Conflict Resolver** — selects the latest effective authorized document.
* **Security Query Guardrails** — blocks sensitive requests such as credential access and unauthorized payroll/PII requests.
* **Evidence + Citations** — identifies the authorized documents used for the answer.
* **Audit Trail** — records requests, authorization decisions, evidence IDs, and security violations.

**What are you deliberately NOT doing?**

We are not building a complete enterprise document-management system, training our own LLM, or allowing the LLM to access unauthorized documents. Production SSO and enterprise identity integration are also outside the current prototype.

---

## 5. Why an Agentic Approach?

**What does your agent decide or do on its own?**

The research workflow analyzes the employee query, retrieves relevant authorized evidence, checks security constraints, selects the latest valid evidence, prepares the permitted context, generates an answer, and records the decision.

**Why wouldn't a fixed script, if-else rules, or a simple chatbot be enough?**

Enterprise research questions can require multiple steps: retrieving relevant documents, applying authorization, comparing versions, selecting valid evidence, and generating a cited response. A controlled agent workflow combines these steps while keeping security checks outside the LLM.

---

## 6. Who It's For & What Changes

**Who or what is this for?**

Enterprise employees and organizations that need secure and reliable access to internal knowledge.

**The world today, without your solution:**

Employees may need to search multiple internal systems manually, while an AI assistant without authorization-aware retrieval could expose information from documents the employee is not permitted to access. Outdated versions and conflicting information can also produce unreliable answers.

**The world with your solution, fully built and scaled to production:**

Employees can ask questions naturally and receive answers based only on authorized evidence. Organizations can enforce access policies before AI processing while maintaining an audit trail of requests and evidence.

**What your hackathon build actually delivers today:**

A working Streamlit prototype that accepts employee questions, applies access-control checks, retrieves permitted documents, handles document versions, generates evidence-backed answers, blocks sensitive requests, refuses inaccessible information, and records security/audit information.

**Before vs. After**

| What Changes         | Today                                  | With Our Current Build                            | At Production Scale                       |
| :------------------- | :------------------------------------- | :------------------------------------------------ | :---------------------------------------- |
| Data access security | Permissions may be checked separately  | Authorization is enforced before LLM evidence     | Centralized enterprise policy enforcement |
| Sensitive requests   | Manual/security-policy dependent       | Query guardrails block defined sensitive requests | Enterprise DLP and policy engine          |
| Outdated information | Employees may encounter older versions | Latest authorized version is selected             | Automated document lifecycle management   |
| Auditability         | Limited/manual tracking                | Requests and security decisions are logged        | Compliance-grade centralized audit system |

---

## 7. Architecture & Agents

**How is your system put together?**

Employee → Streamlit UI → Research Agent → Query Guardrails → Authorized Retrieval → Security-Level Check → Version Resolver → Authorized Evidence → LLM → Answer + Citations → Audit Log.

### 7.1 Agents

* **Research Agent:** Coordinates the research workflow. It validates the query, retrieves permitted evidence, selects the latest authorized document, prepares the LLM context, generates the response, and records the decision.

* **Security Guardrail:** Checks sensitive queries before retrieval and blocks unauthorized requests such as credential access or restricted payroll/PII requests.

### 7.2 Services, APIs, Databases & Memory

* **Authorization Service:** Checks user clearance, department, role, and document classification before content is used.
* **RBAC Service:** Maps prototype roles to security levels and permitted information categories.
* **Retrieval Service:** Searches authorized documents using query/document relevance matching and security filtering.
* **Versioning Service:** Selects the latest effective version from authorized matching documents.
* **LLM Service:** Builds a prompt using only authorized evidence and generates the final response.
* **Audit Service:** Records requests, authorization decisions, evidence IDs, and sources.
* **Security Audit Service:** Stores blocked security attempts in a CSV audit log.
* **Document Storage:** JSON files store sample users and enterprise documents.

**How does your system remember things (memory & state)?**

The prototype does not use conversational memory. It maintains document metadata, user permissions, and audit records as persistent local JSON/CSV state so each request can be independently authorized and audited.

**Diagram Link (Optional):** N/A

### 7.3 Example Walkthrough

**Example input:**
U102 asks: "What is the Q4 revenue forecast?"

1. **Employee/UI** submits the natural-language question with the selected user context.
2. **Security Guardrail** checks whether the query contains a blocked sensitive request.
3. **Retrieval Service** searches documents while applying the user's authorization and security level.
4. **Version Resolver** selects the latest authorized matching evidence.
5. **Research Agent** passes only the authorized evidence to the LLM.
6. **LLM Service** generates an answer using only the supplied authorized evidence.
7. **Audit Service** records the request, authorization decision, and evidence used.

**Final output:**
"Q4 projected revenue is 120 crore." with citation to DOC-101, version 2.0.

**Anything special about how your workflow runs?**

The most important security boundary occurs before the LLM. The LLM never receives unauthorized document content and is instructed to answer only from the authorized evidence supplied by the application.

---

## 8. Tech Stack

| Layer                | Technology                                           |
| :------------------- | :--------------------------------------------------- |
| Frontend / Interface | Streamlit                                            |
| Backend              | Python                                               |
| Agent Framework      | Custom Python agent workflow                         |
| Database / Storage   | JSON documents/users + CSV security audit log        |
| Hosting              | Streamlit Community Cloud                            |
| LLM                  | OpenAI API integration with local mock/fallback mode |
| Authorization        | Custom RBAC + document-level authorization           |
| Version Handling     | Custom Python version resolver                       |
| Testing              | Pytest                                               |
| Source Control       | Git + GitHub                                         |

---

## 9. What to Expect From Our Current Build

**Working:**

* Streamlit web interface.
* Natural-language employee queries.
* User and role selection for the prototype.
* Document classification and authorization checks.
* Role-based security levels.
* Pre-LLM document filtering.
* Unauthorized document protection.
* Sensitive-query guardrails.
* Version-aware evidence selection.
* Authorized evidence passed to the LLM.
* Answer citations showing document ID, title, version, and effective date.
* Audit logging.
* Security violation logging.
* Admin Security Console.
* Automated test suite with **23 passing tests**.
* Test scenarios covering authorization, retrieval, versions, RBAC, guardrails, and security levels.
* Deployed Streamlit prototype.

**Partly working, mocked, or hard-coded:**

* The prototype uses sample JSON documents and users rather than a live enterprise document repository.
* Identity and role selection are provided through the demo interface rather than production authentication.
* The LLM supports an OpenAI API integration, with a local evidence-based fallback when no API key is configured.
* Retrieval currently uses lightweight keyword-based matching rather than a production vector database.

**Not working or not built yet:**

* Production enterprise SSO/OAuth authentication.
* Live enterprise identity/HR integration.
* Production-scale vector database.
* Real-time enterprise document ingestion.
* Production-grade distributed audit storage.
* Full document lifecycle and access-policy management.

**What we'd most like to be judged on:**

Our core security design: **authorization happens before LLM access**. Unauthorized documents are filtered out before their content can become LLM evidence, rather than relying on the LLM to decide what information an employee is allowed to see.

---

## 10. Future Scope

### Idea 1

**Name:** Permission-Aware Query Rewriting

**What it is:** The agent detects when a question requires inaccessible information and reformulates it to find the closest useful answer using only authorized evidence.

**Why it matters:** Users can still receive useful information without exposing protected details.

**How we'd build it:** Add a query-planning component that maps required evidence to access permissions and generates a safe alternative query.

**Done when:** A restricted query produces the closest useful answer from authorized evidence without revealing protected details.

### Idea 2

**Name:** Continuous Access Monitoring

**What it is:** Continuously monitors employee permissions and updates document access when roles, departments, or clearance levels change.

**Why it matters:** Prevents outdated permissions from continuing to grant access to sensitive information.

**How we'd build it:** Connect the authorization engine with enterprise identity and HR systems and re-evaluate permissions dynamically.

**Done when:** Changing a user's enterprise role automatically changes the documents available to the research agent.

### Idea 3

**Name:** Enterprise Vector Retrieval

**What it is:** Replace the prototype keyword search with a permission-aware vector retrieval system for large document collections.

**Why it matters:** Improves semantic search quality while maintaining authorization boundaries.

**How we'd build it:** Add embeddings and a vector database with document-level access metadata enforced before content reaches the LLM.

**Done when:** Large document collections can be searched semantically while unauthorized documents remain excluded from LLM evidence.

---

## 11. Additional Notes

The current implementation is intentionally presented as a security-focused prototype. The selected employee identities and roles are demo controls rather than production authentication. Production deployment would integrate enterprise SSO, centralized identity management, dynamic authorization policies, secure document storage, and enterprise audit infrastructure.

### Demonstrated Test Scenarios

**Test A — Authorized Answer**

User U102, Finance, asks for the Q4 revenue forecast. The system retrieves DOC-101 because the document is authorized for the user and returns the authorized forecast of **120 crore** from version 2.0.

**Test B — Relevant but Unauthorized**

User U205, Marketing, asks for the Q4 revenue forecast. The matching restricted document is not authorized for the user. The system returns **ACCESS DENIED** and sends **no document evidence to the LLM**.

**Test C — Authorized Conflict**

User U301, Finance, asks for the latest Q4 forecast. Both authorized versions are considered, and the system selects DOC-302, version 2.0, effective 2026-09-01, with the authorized forecast of **125 crore**.

**Key Security Principle:**

> Authorization is enforced before information reaches the LLM.

**Project Links:**

**GitHub Repository:** https://github.com/rebbajahnavi/secure-enterprise-ai-research-agent

**Live Demo:** https://secure-enterprise-ai-research-agent-fastandcurious.streamlit.app/
