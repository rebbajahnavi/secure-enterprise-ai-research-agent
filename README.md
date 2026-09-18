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

Documents may also contradict each other, be outdated, have different versions, or contain incomplete information.

**Critical requirement**

An unauthorized document must **never be provided to the LLM simply because it is relevant to the question**.

## The Challenge

Build a secure enterprise research agent that answers employee questions over internal documents while enforcing authorization. Relevant information that the requesting employee is not authorized to access must never be provided to the language model or revealed in the final answer.

---

## 3. TL;DR

**Problem:** AI assistants can leak sensitive enterprise data when retrieval ignores employee access permissions.

**Solution:** Our secure research agent applies authorization **before** LLM processing, filters evidence by access level, selects the latest authorized version, provides citations, and records audit information.

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
* **Latest Authorized Version Selection** — selects the latest effective authorized document.
* **Security Query Guardrails** — blocks sensitive requests such as credential access and unauthorized payroll/PII requests.
* **Evidence + Citations** — identifies the authorized documents used for the answer.
* **Audit Trail** — records requests, authorization decisions, evidence IDs, and security violations.

**What are you deliberately NOT doing?**

We are not building a complete enterprise document-management system, training our own LLM, or allowing the LLM to access unauthorized documents. Production SSO and enterprise identity integration are also outside the current prototype.

---

## 5. Why an Agentic Approach?

**What does your agent decide or do on its own?**

The research workflow analyzes the employee query, retrieves relevant authorized evidence, checks security constraints, selects the latest authorized evidence, prepares the permitted context, generates an answer, and records the decision.

**Why wouldn't a fixed script or a simple chatbot be enough?**

Enterprise research requires a multi-step secure pipeline: retrieval $\rightarrow$ authorization $\rightarrow$ latest authorized version selection $\rightarrow$ cited generation. A controlled agent workflow ensures security checks remain **outside** the LLM's decision-making process.

---

## 6. Who It's For & What Changes

**The world today, without your solution:**
AI assistants without authorization-aware retrieval can expose sensitive data. Outdated versions and conflicting information produce unreliable answers.

**The world with your solution, fully built and scaled to production:**
Employees receive answers based only on authorized evidence. Organizations enforce access policies before AI processing while maintaining a compliance-grade audit trail.

**Before vs. After**

| What Changes         | Today                                  | With Our Current Build                            | At Production Scale                       |
| :------------------- | :------------------------------------- | :------------------------------------------------ | :---------------------------------------- |
| Data access security | Permissions checked separately         | Authorization enforced before LLM evidence       | Centralized enterprise policy enforcement |
| Sensitive requests   | Manual/policy dependent               | Query guardrails block sensitive requests          | Enterprise DLP and policy engine          |
| Outdated information | Employees encounter older versions     | Latest authorized version is selected             | Automated document lifecycle management   |
| Auditability         | Limited/manual tracking                | Requests and security decisions are logged        | Compliance-grade centralized audit system |

---

## 7. Architecture & Agents

**System Flow:**

```mermaid
graph TD
    User[Employee / Streamlit UI] --> Agent[Research Agent]
    Agent --> SG[Security Guardrail]
    SG -- Blocked Request --> AL[Audit & Security Log]
    SG -- Authorized Query --> AR[Authorized Retrieval]
    AR --> SLC[Security-Level Check]
    SLC --> VS[Version Selection]
    VS --> AE[Authorized Evidence]
    AE --> LLM[LLM Service]
    LLM --> Ans[Answer + Citations]
    Ans --> AL
