# Testing policy state

This directory contains the durable, reviewed inputs to `testpolicy`:

- `project.json` declares active lifecycle profiles and owners;
- `claims.json` declares product claims and their policy categories;
- `architecture.json` maps changed paths to components, boundaries, and claims;
- `commands.json` names validated project-native commands, arguments, and
  timeouts used by mechanical obligations;
- `policies.json` contains project-specific additions and justified
  not-applicable overrides;
- `decisions/` retains accepted profile and threshold decisions;
- `waivers/` and `attestations/` contain owned, expiring exception or human
  evidence records when created.

Generated run evidence belongs under `.cache/`, not here.
