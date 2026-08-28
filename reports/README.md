# Reports

Reports are reviewed evidence summaries. Raw model responses stay under the ignored results directory.

Included reports:

- qwen35_windows_development_v1.md — historical development baseline.
- 2026-08-28-qwen25-targeted-v2-windows-install-smoke.md — installation and native tool-call smoke test.
- 2026-08-28-qwen25-targeted-v2-asb-lifecycle.md — ASB UI lifecycle, context limitation, parameter analysis, wiring, packaging and non-default EXE verification.

The targeted Qwen2.5 v2 model has not been scored on the complete frozen holdout_v1 set. Do not claim a holdout score until the full harness has run.

Every future report should include model ID, quantization, operating system, backend, effective context, temperature, concurrency, case-set commit SHA and raw-result hash. Remove credentials, usernames and machine-specific paths before publication.
