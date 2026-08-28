# Factory security surface (qc-security)

## Threat model (factory, not product SaaS)

| Surface | Risk | Check |
|---------|------|-------|
| Secrets in tree | Key leak | API key / private key patterns |
| Shell command runners | Injection / shell=True | Prefer `pipeline.shell_safety.shell_run_kwargs` |
| Write roots | Pack/constitution mutate | Refuse constitution.yaml / process_packs writes |
| Live network defaults | Unintended egress | `--allow-live` / `allow_live=True` default off |
| Dual-gate crowns | Auto field_proven | Prefer qc-honesty for stamps |

## Doctrine refs

- `notes/ops/dual_gate_contract.md`
- Research refuse lists (handoff / candidates)

## Known good

- `pipeline/shell_safety.py` — `shell_run_kwargs`
- Engines should import shell_safety for CLI runs

## Non-claims

Not full SAST/SCA, not pen test, not product auth productization.
