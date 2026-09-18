# The Employee Who Asked for Too Much

## Team Details

**Team Name:** Fast & Curious

**Team Members:** [Add all 5 team member names]

---

## Problem Statement

**The Employee Who Asked for Too Much**

Company internal documents contain information with different sensitivity levels such as Public, Internal, Confidential, and Restricted. Employees have different permissions based on their roles and access levels.

The challenge is to build an AI research assistant that can search enterprise documents and answer employee questions while ensuring that employees never receive information they are not authorized to access.

A critical requirement is that unauthorized document content must never be passed to the LLM merely because it is relevant to the user's question.

---

## TL;DR

We built a secure enterprise AI research assistant that answers employee questions using company documents while enforcing authorization before information reaches the AI model.

The system combines role-based access control, document-level authorization, security-level filtering, query guardrails, version-aware evidence selection, source citations, and security audit logging.

Unauthorized or sensitive requests are blocked before the LLM receives any evidence.

The prototype demonstrates authorized information retrieval, prevention of restricted information disclosure, and selection of the latest authorized document version.

---

## Scope

### In Scope

* Natural-language questions from employees
* Predefined employee identities and roles for prototype demonstration
* Role-based permissions
* Document classification and security levels
* Document-level authorization
* Security-level filtering during retrieval
* Query guardrails for sensitive requests
* Protection against requests for credentials, payroll, PII, and executive-private information
* Retrieval of authorized documents
* Latest-version selection for conflicting or outdated authorized documents
* Answers based only on authorized evidence
* Source citations
* Request and security audit logging
* Admin security console for reviewing blocked attempts
* Streamlit-based demonstration interface

### Out of Scope

* Production-grade employee authentication
* Enterprise SSO integration
* Full enterprise document-management integration
* Production-scale vector databases
* Automated ingestion from live corporate systems
* Production deployment
* Compliance certification
* Enterprise-wide identity and access management

---

## Why is this Agentic?

The system follows a controlled research workflow rather than directly sending a user's question to an LLM.

For each request, the workflow:

1. Receives the user's question and identity/role context.
2. Validates the query against security guardrails.
3. Retrieves candidate information from enterprise documents.
4. Applies authorization and security-level checks.
5. Removes inaccessible information before LLM processing.
6. Selects the latest authorized version when multiple authorized documents exist.
7. Builds an evidence set using only authorized documents.
8. Sends only that authorized evidence to the LLM.
9. Generates an answer with source information.
10. Records the request and authorization decision in the audit log.

This controlled sequence allows the research process to make authorization-aware decisions before AI generation.

---

## Target Audience

The prototype is designed for organizations where employees need to search internal information while respecting access-control policies.

Potential users include:

* Employees
* Managers
* Security teams
* IT administrators
* Compliance teams
* Enterprise knowledge-management teams

The prototype particularly demonstrates how a security-conscious AI assistant can be used in an enterprise environment.

---

## Architecture

The core security architecture is:

```text
Employee
   ↓
Streamlit UI
   ↓
Research Agent
   ↓
Query Security Guardrails
   ↓
Document Retrieval
   ↓
Authorization + Security-Level Check
   ↓
Latest Authorized Version Selection
   ↓
Authorized Evidence Only
   ↓
LLM
   ↓
Answer + Sources
   ↓
Audit Logging
```

The most important security boundary is between retrieval and LLM processing.

The system follows:

```text
Search
  ↓
Authorization Filter
  ↓
Remove Unauthorized Documents
  ↓
Version / Conflict Check
  ↓
Authorized Evidence
  ↓
LLM
```

It does **not** follow:

```text
Search
  ↓
All Documents
  ↓
LLM
  ↓
Ask LLM to decide what the user can see
```

This prevents unauthorized document content from being supplied to the LLM.

---

## Agents

### Research Agent

The Research Agent coordinates the secure research workflow.

Its responsibilities include:

* Receiving the user question
* Running security validation
* Calling authorized retrieval
* Selecting the latest authorized evidence
* Preparing the LLM request
* Generating the response
* Returning source information
* Recording the authorization decision

### Security Guardrail

The security guardrail checks potentially sensitive requests before the normal research workflow continues.

Examples include requests involving:

* Salary
* Payroll
* Passwords or credentials
* PII
* Executive-private information

Blocked requests are logged as security violations.

---

## Services

### Authorization Service

The authorization layer checks:

* User clearance
* Document classification
* Department
* Role
* Document access metadata

A document is returned only when the user's access requirements are satisfied.

### RBAC Service

The prototype includes four demonstration roles:

| Role         | Access Level |
| ------------ | -----------: |
| Intern       |            1 |
| Manager      |            2 |
| HR Admin     |            3 |
| System Admin |            4 |

Permissions are mapped to the role.

### Retrieval Service

The retrieval service searches documents using the user's question while applying authorization and security-level filtering.

Documents above the user's permitted security level are excluded.

### Versioning Service

When multiple authorized documents contain different versions of related information, the system selects the latest version using the effective date and version number.

### LLM Service

The LLM receives only the authorized evidence selected by the secure workflow.

The prompt explicitly instructs the model to use only the supplied authorized evidence.

### Audit Service

The system records request information, authorization decisions, selected evidence, and security violations.

---

## Memory

The prototype uses document metadata and local audit records rather than persistent conversational memory.

Documents contain metadata such as:

* Document ID
* Title
* Classification
* Security level
* Allowed departments
* Allowed roles
* Version
* Effective date
* Content

Security audit records contain:

* Timestamp
* User role
* Query
* Violation type

This allows the prototype to maintain traceability of security-related requests.

---

## Example Workflow

### Scenario 1 — Authorized Request

**User:** U102
**Role:** Manager
**Question:** What is the Q4 revenue forecast?

The system identifies an authorized Finance document:

**DOC-101 — Q4 Revenue Forecast — Version 2.0**

The document is allowed through the authorization layer.

Only DOC-101 is provided as LLM evidence.

The assistant returns the authorized forecast information and cites DOC-101.

---

### Scenario 2 — Restricted Information

**User:** U205
**Role:** Manager
**Question:** What is the Q4 revenue forecast?

A Restricted Executive-only document contains a different forecast.

However, the user's authorization does not permit access to that document.

The document is removed before LLM processing.

The result is:

```text
ACCESS DENIED
LLM Evidence: None
```

The restricted value is not disclosed.

---

### Scenario 3 — Conflicting Authorized Versions

**User:** U301
**Role:** Manager
**Question:** What is the Q4 forecast?

Two authorized documents exist:

```text
DOC-301
Version: 1.0
Effective: 2026-06-01
Forecast: ₹110 crore

DOC-302
Version: 2.0
Effective: 2026-09-01
Forecast: ₹125 crore
```

The system selects the latest authorized document, DOC-302.

The LLM receives DOC-302 as the evidence and the assistant returns the latest authorized forecast.

---

## Security Design

Security is enforced before LLM generation.

### Authorization Before LLM

The LLM does not receive the complete document collection.

Only authorized evidence is included in the LLM request.

### Sensitive Query Guardrails

Potentially sensitive requests are checked before retrieval proceeds.

Blocked requests do not generate an LLM evidence set.

### Anti-Jailbreak Handling

The system also checks for attempts to bypass the security workflow, such as requests to ignore existing instructions or act as an administrator.

Such requests are blocked rather than allowing the user to bypass the authorization workflow.

### No Confirmation of Restricted Information

When the user does not have access, the system does not reveal the restricted document's contents.

The response indicates that accessible information is unavailable rather than exposing protected information.

### Security Audit

Blocked security attempts are recorded in a local security audit CSV.

The Admin Console displays the recorded security events for authorized administrative demonstration roles.

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI

* OpenAI API integration
* Mock/fallback response mode for prototype demonstration when an API key is not configured

### Retrieval

* Python-based document retrieval
* Metadata-based authorization filtering

### Security

* Role-Based Access Control (RBAC)
* Document-level authorization
* Security-level filtering
* Query guardrails
* Audit logging

### Data

* JSON documents and user metadata
* CSV security audit log

### Testing

* Pytest

### Version Control

* Git
* GitHub

---

## Current Build

The current prototype includes:

* Streamlit research interface
* User and role selection for demonstration
* Role-based permission mapping
* Document classification
* Security-level metadata
* Authorization filtering
* Security guardrails
* Anti-jailbreak blocking
* Version-aware document selection
* Authorized-only LLM evidence
* Source citations
* Request audit logging
* Security violation logging
* Admin Security Console
* Automated test suite
* GitHub repository
* Streamlit deployment

The prototype has been tested against the main authorization, retrieval, versioning, LLM, RBAC, guardrail, and security-level scenarios.

---

## Testing

The automated tests cover:

* Authorization decisions
* Document retrieval
* Version selection
* Security behavior
* LLM evidence handling
* RBAC role levels
* Role permissions
* Query guardrails
* Security-level filtering

The primary demonstration scenarios are:

| Test                                                       | Expected Result                    |
| ---------------------------------------------------------- | ---------------------------------- |
| Authorized Finance request                                 | Authorized information returned    |
| Marketing user requesting Restricted Executive information | Access denied                      |
| Multiple authorized versions                               | Latest authorized version selected |
| Sensitive payroll request                                  | Security violation                 |
| Credential/password request                                | Security violation                 |
| Security-level violation                                   | Document filtered before LLM       |

---

## Auditability

Every research request records relevant information such as:

* User ID
* Query
* Authorization status
* Selected evidence
* Sources
* Timestamp

Security violations additionally record:

* Timestamp
* User role
* Query
* Violation type

This provides an audit trail for demonstrating how security decisions were made.

---

## Why This Approach is Secure

The central security principle is:

> **Authorization happens before information reaches the LLM.**

The LLM is therefore not responsible for deciding whether a document should be accessible.

Instead, the application determines what evidence the user is authorized to receive and only then constructs the LLM request.

This creates a clear security boundary between enterprise data access and AI generation.

---

## Future Scope

Future versions could include:

* Enterprise SSO authentication
* Integration with corporate identity providers
* Real employee directory integration
* Production vector databases
* Enterprise document-management connectors
* More advanced semantic retrieval
* Attribute-Based Access Control (ABAC)
* Fine-grained document and field-level permissions
* Encryption and key-management integration
* More comprehensive policy engines
* Continuous security monitoring
* Production-grade audit infrastructure
* Human approval workflows for highly sensitive requests

---

## Prototype Limitations

This is a hackathon prototype rather than a production enterprise security system.

User identities and roles are currently selected through the demonstration interface rather than verified through a production authentication system.

The document collection is local and intentionally small so that the authorization workflow and security behavior can be demonstrated clearly.

Production deployment would require integration with enterprise identity, document-management, policy, monitoring, and compliance systems.

---

## Demo

**Deployed Prototype:**

[Secure Enterprise AI Research Agent — Streamlit](https://secure-enterprise-ai-research-agent-fastandcurious.streamlit.app/?utm_source=chatgpt.com)

**GitHub Repository:** [Paste your GitHub repository link here]

### Recommended Demo Evidence

Include screenshots demonstrating:

1. **Authorized request** — authorized answer with source document.
2. **Restricted request** — `ACCESS DENIED` with `LLM Evidence: None`.
3. **Latest-version selection** — DOC-302, Version 2.0, with the latest authorized forecast.
4. **Security violation** — blocked sensitive or jailbreak-style request.
5. **Admin Security Console** — security audit records.

---

## Conclusion

The prototype demonstrates an authorization-aware enterprise AI research workflow in which security decisions are enforced before LLM generation.

The key design principle is that the AI model should only receive evidence that has already passed the application's authorization checks.

This allows the system to provide useful enterprise research capabilities while maintaining a clear separation between document access control and AI generation.
