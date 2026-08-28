# Leaf aim template for /lfg

```text
Ship an offline/sandbox module for leaf `<id>` (`<name>`).

Process: <summary>
Inputs: <list>
Outputs: <list>
Metrics: <list or none>
Depends on: <ids>

Success criteria:
- Automated tests or fixtures prove the I/O contract
- Harsh critic ACCEPT on the leaf module only
- Document how a later orchestrator would call it (CLI/API/path)

Non-goals:
- Live capital, live orders, unsupervised production trading
- Replacing human_only parents (e.g. CIO/CRO/CCO/PM authority, fundraising)
- Claiming investment alpha or regulatory sign-off
- Expanding scope to sibling leaves

Interface hint: <from DE pack if any>
```
