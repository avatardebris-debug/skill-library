# field_tests.md contract (pipeline-compatible)

Parsed by `pipeline/field_test_runner.py` → `parse_field_tests_md`.
Baseline B1/B2/B3 are added by the runner — **do not** redefine them as P/I tasks.

## File location

```text
<project_root>/phases/ship/field_tests.md
```

## Template

```markdown
# Field Tests

## Product tests
- [ ] Task P1: <short title>
  - Kind: product
  - Command: `<absolute-python> -m <package>.main --help`
  - Expect: exit 0

- [ ] Task P2: <short title>
  - Kind: product
  - Command: `<absolute-python> -c "from pkg.mod import fn; print(fn())"`
  - Expect: <stable substring>

## Integration tests
- [ ] Task I1: <short title>
  - Kind: integration
  - Command: `<absolute-python> ...`
  - Expect: exit 0
```

## Rules (strict)

| Field | Rule |
|-------|------|
| Checkbox | `- [ ] Task P1:` or `- [ ] Task I1:` (IDs `P1`…`P8`, `I1`…`I4`) |
| Kind | only `product` or `integration` |
| Command | single shell command; workspace root cwd; inside backticks after `Command:` |
| Expect | `exit N` **or** short stable stdout/stderr substring **or** `keys` / `forbid` (see `notes/ops/use_list/STRUCTURED_EXPECT.md`) |
| Python | absolute interpreter path on every Command line |
| Modules | only packages/files that exist under workspace |
| OS | prefer `python -m` / `python -c`; avoid bash-only pipelines on Windows |

## Expect parsing

- `Expect: exit 0` → require return code 0
- `Expect: Hello` → require return code 0 **and** substring in combined stdout/stderr
  (whitespace-collapsed, case-insensitive fallback)
- `Expect: keys mer,fund_code,returns` → stdout JSON must contain those keys (dotted in)
- `Expect: forbid /rc` → combined stdout/stderr must **not** contain the literal
  Spec: `notes/ops/use_list/STRUCTURED_EXPECT.md`. Applied by `field_test_runner`.
  A second `- Expect:` on the same task is allowed (e.g. two forbids).
  Helper pass is mechanical, not `field_proven`.


## Counts

- Product: ~4–8 solid tests
- Integration: ~2–4
- Quality over quantity

## Dual-gate min bars (factory `field_prove_gate`)

Defaults (env `FIELD_MIN_PRODUCT` / `FIELD_MIN_INTEGRATION`):

- ≥ **1** non-trivial **product** (`P*`) task
- ≥ **1** non-trivial **integration** (`I*`) task
- Non-trivial = real Command + Expect, **not** only `--help` / `py_compile` / bare `import … print(IMPORT_OK)`
- Baseline **B*** never counts toward bars and never alone → `field_proven`

Mechanical runner pass → `field_test_passed`.  
`field_proven` needs runner pass + Adequacy ADEQUATE + min bars.

## Results file (skill / runner)

```text
<project_root>/phases/ship/field_test_results.md
```

Include per-task PASS/FAIL, command, and output tail. End with:

```markdown
## Verdict: PASS
```

or `## Verdict: FAIL`.

## What not to put in the plan

- Baseline B1/B2/B3 duplicates
- Prose-only plans without Task + Command + Expect
- Network/paid APIs as required without dry-run/mock
- Interactive prompts
- Paths outside workspace (except OS temp for outputs if needed)
