# Delegation guide

Use this only when the compact policy does not clearly place the work. The aim is fewer Sol execution tokens without weakening Sol's decisions.

## Mapping

| Work | Owner | Reason |
| --- | --- | --- |
| Find callers, usages, or affected tests | Luna | Bounded search with inspectable evidence. |
| Implement a named function against existing tests | Luna | Explicit contract and pass condition. |
| Apply a mechanical edit across many files | Luna | Much execution, little judgment. |
| Run tests and isolate a failure | Luna | Commands and evidence constrain the answer. |
| Review a finished change for missed cases | Luna, then Sol | Luna expands coverage; Sol judges significance. |
| Convert an agreed design into one component | Luna | Sol already made the costly design decision. |
| Interpret a vague request | Sol | A wrong interpretation poisons downstream work. |
| Choose architecture or data ownership | Sol | Cross-cutting and expensive to reverse. |
| Debug an unknown interaction | Sol first | Delegate after narrowing the fault domain. |
| Integrate worker changes or decide completion | Sol | Requires the whole objective and tradeoffs. |

## Brief packing

Good:

```text
Update parse_date() in src/date.py to accept ISO dates with Z.
Keep naive-date behavior unchanged. Tests are in tests/test_date.py.
Success: that file's tests pass.
Return only outcome; changed paths or file:line evidence; verification and result; real blocker or risk. Do not narrate or paste available diffs.
```

Wasteful: repository history, the lead's investigation diary, code Luna can read, repeated requirements, or a request for a long report. A brief should transfer the contract, not the lead's entire context.

## Routing trial

A ten-scenario comparison on 2026-08-31 had Luna xhigh and Sol high agree on the clear cases: mechanical rename, caller tracing, contract-driven implementation, and test isolation went to Luna; architecture stayed with Sol. The useful disagreements were:

| Scenario | Decision |
| --- | --- |
| Two direct repository searches | Sol, because briefing costs more than the work. |
| Deadlock with unknown fault domain | Sol until the fault domain is narrow. |
| Review three patches and decide completeness | Luna may check coverage; Sol decides completeness. |
| Apply an approved design to three adapters | Luna implements; Sol integrates. |

Luna tended to accept executable work even when delegation was uneconomical. One bounded review also stalled for over 90 seconds and returned nothing, which supports stopping rather than automatically retrying.

These are routing observations, not a price benchmark. Cached instructions and repository context differed between runs. Judge economy by whether the Sol brief plus review is cheaper than direct Sol execution.
