# Infrastructure Surface

This directory is reserved for runtime bootstrap assets, future Canton or Quickstart overlays, and other environment wiring that must stay separate from policy and workflow code.

Current intent:

- keep topology and environment configuration out of domain logic
- make future LocalNet or Quickstart overlays land under `infra/`
- preserve reproducible bootstrap and demo commands
