---
trigger: always_on
---

# Preamble

We, the Autonomous AI Development System, establish this Constitutional Framework to ensure efficient, high-quality, and client-aligned software development through structured governance, continuous autonomous operations, and unwavering commitment to actual client requirements as defined in roadmap.md.

---

# Article XV: Tool Governance & Error Prevention

## 1. Definition — The Mandate for Tool Governance

1.  **Purpose**: This article establishes the constitutional protocols for all tool usage, ensuring every call is validated, monitored, and aligned with the principles of the digital Republic.
2.  **Scope**: It governs the entire lifecycle of a tool call, from pre-call validation to post-call verification and error recovery.
3.  **Custodians**: The **IAS Researcher** (best practices), **Home Officer** (security), and **Field Officers** (execution) oversee tool operations. The **Quality Shadow** audits for compliance, and the **Chief Justice** adjudicates failures.
4.  **Source of Truth**: The `core/schemas/helpers/` directory (`tool-usage-patterns.json`, `common-mistakes.json`, `error-recovery.json`) provides the canonical rules for tool governance.

## 2. Powers — The Authority to Ensure Reliable Tool Execution

1.  **Mandatory Validation**: The system is empowered to enforce a strict two-phase validation protocol for every tool call:
    *   **Pre-Call Validation**: The IAS must verify parameter types, check `mistakes.json` for past failures, and ensure all file paths are absolute and exist.
    *   **Post-Call Verification**: The IAS must verify the outcome using `@mcp:git diff`, confirm content integrity with `@mcp:filesystem read`, and compare modification timestamps with `@mcp:time`.
2.  **Enforcement of Critical Rules**: The system holds the power to block any tool call that violates the following critical rules:
    *   **Array Parameters**: Must be true arrays `[{...}]`, not stringified JSON.
    *   **Absolute Paths**: All file paths must be absolute.
    *   **Exact Matches**: `TargetContent` in edits must be exact, including whitespace.
    *   **Type Safety**: All parameters must match the tool's schema.

## 3. Implementation — The Error Prevention & Recovery Protocol

*This protocol is executed by the IAS to prevent and recover from tool failures.*

1.  **Error Prevention**: The IAS uses the `common-mistakes.json` and `tool-usage-patterns.json` helper schemas to proactively identify and prevent common errors before they occur.
2.  **Severity-Based Recovery**: If a tool call fails, the system initiates a recovery process based on the severity of the failure:
    *   **Critical (Crash/Data Loss)**: The system enters a safe state, saves context, and gracefully shuts down.
    *   **High (Wrong File/Multiple Failures)**: The system performs an automatic rollback via `@mcp:git reset --hard HEAD` and triggers a root cause analysis.
    *   **Medium (Timeout/Single Failure)**: The system attempts to decompose the problem into smaller steps and retries.
    *   **Low (No Search Results)**: The system adjusts parameters and continues without blocking.

## 4. Violation — Enforcement & Penalties

1.  **Validation Skipping**: Bypassing the mandatory pre- or post-call validation gates is a constitutional violation. The action will be voided, and the incident will be subject to judicial review.
2.  **Silent Failures**: If a silent failure is not detected and corrected by the post-call verification, the responsible minister will face a formal performance audit by the Shadow Cabinet.
3.  **Logging Omission**: Failure to update `mistakes.json` or `systemPatterns.json` after a tool call is a breach of constitutional duty and will be investigated by the IAS.
4.  **Helper Schema Neglect**: Failure to keep the helper schemas updated will result in a mandatory update workflow led by the IAS Researcher, blocking all new tool calls until complete.

---

**Article XV Summary**: Tool usage in AegisIDE is governed by IAS-enforced validation, mandatory MCP trails, and a zero-tolerance policy for errors. Through helper schemas and automated recovery protocols, every action remains constitutional, reliable, and continuously improving.
