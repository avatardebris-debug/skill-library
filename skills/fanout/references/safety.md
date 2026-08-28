# Fanout safety

| Rule | Practice |
|------|----------|
| No live money path by default | Paper/sandbox modules only |
| human_only never selected | Unless --force-human with loud log |
| Dependency order | Topo sort; skip if unmet |
| Harsh critic | Default for leaf ship |
| Registry for compose | status + module_path required for shipped |
