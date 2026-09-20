# Agent Reliability Pilot

## Outcome
Turn one existing tool-using AI workflow from an impressive demo into a controlled production candidate.

## What is delivered in 10 working days
1. A map of the agent's tools, permissions, state transitions, external side effects, and failure modes.
2. A replayable evaluation suite covering happy paths, malformed inputs, ambiguous requests, tool/API failures, duplicate events, prompt injection attempts, and approval-required actions.
3. Structured output contracts and validation gates for every action that changes data or contacts an external system.
4. Idempotency keys, bounded retries, timeout handling, audit logs, and human approval/escalation paths.
5. A simple scorecard: task success, unsafe-action rate, tool failure rate, and escalation rate.
6. A written remediation plan and a handover session.

## Client keeps control
- No production credentials are needed for the initial audit.
- Evaluation can run against scrubbed examples or a staging environment.
- The client chooses which actions are autonomous and which require approval.
- Source code and test cases stay with the client.

## Fixed-scope pilot
- One workflow
- Up to five tools or integrations
- Up to 40 representative test cases
- 10 working days
- Starting at USD 750 / EUR 700, adjusted only if the workflow exceeds the scope above.

## Why this work is different
The focus is not prompts or a generic chatbot. It is the software layer that makes an agent accountable: typed data, explicit permissions, controlled execution, retries, observability, and a human fallback.

## Relevant implementation experience
This pilot draws on the same production-oriented approach used in Advanced-RAGv2: tool-using agent workflows, generated-code execution in a sandboxed environment, FastAPI services, retrieval, validation, and controlled agent behavior.

## Discovery questions
1. Which customer or internal action can the agent perform today?
2. What is the cost of the wrong action?
3. Which integrations can create, change, send, or delete something?
4. Do you have real examples of failures, escalations, or manual corrections?
5. What must be true before this workflow can be deployed more widely?
