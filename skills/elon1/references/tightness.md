# Tightness ladder (borrowed)

Source of truth for Elon1 implement. Not the ponytail GitHub plugin.
Lazy about the solution, not about reading.

After you understand the problem (read the task and the code it touches), stop
at the **first** rung that holds:

1. Does this need to exist? → skip (YAGNI)
2. Already in this codebase? → reuse
3. Stdlib? → use it
4. Native platform feature? → use it
5. Already-installed dependency? → use it
6. One line? → one line
7. Only then: the minimum that meets **keep + load-bearing** falsifiers

Never cut: trust-boundary validation, data-loss handling, security,
accessibility, one runnable check for non-trivial logic.

Mark a deliberate corner with a short ceiling + upgrade path, not an essay.

When falsifiers pass: **STOP**. Do not add.
