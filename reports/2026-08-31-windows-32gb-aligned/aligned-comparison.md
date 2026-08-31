# Windows 32 GB aligned ASB benchmark — 2026-08-31

## Decision

**Current status: PASS pending PW-CLICK-01.**

Under ASB's intended operating condition—attended development, human review of AI-proposed actions, then deterministic packaging—the Qwen safety and formatting findings are quality/review-cost observations, not release blockers. Sealed-blind isolation is benchmark governance, not a product runtime defect.

Once PW-CLICK-01 passes the observable-effect gate described below, this benchmark qualifies as **PASS** under the stated product condition.

## Controlled conditions

- Host: Windows 10.0.26200, 32 GB RAM, Python 3.11.9
- Model: asb-qwen25-targeted-v2:q4_k_m, 7.6B, Q4_K_M
- Temperature: 0.1; concurrency: 1
- Formal Qwen route: ASB OpenAI-compatible proxy with ASB normalization
- Native Ollama-direct results: excluded from formal scoring
- Trusted-agent delegation: not used
- Credentials in published evidence: none

## Results

| Layer | Route | Result | Interpretation |
|---|---|---:|---|
| MCP discovery | ASB | 222/222 tools | 40 direct Playwright tools |
| Relay/CDP | ASB Playwright | PASS | healthy, browser ready, CDP reachable and attached |
| Released holdout | Codex direct | 60/60 (100%) | strong-model capability ceiling; latency not comparable |
| Released holdout | Qwen via ASB, run 1 | 46/60 (76.67%) | normalized route |
| Released holdout | Qwen via ASB, run 2 | 45/60 (75.00%) | normalized route |
| Real page execution | Codex via ASB, strict | 6/8 (75%) | P06/P07 blocked by PW-CLICK-01 |
| Real page execution | Codex via ASB, assisted | 8/8 (100%) | two explicit DOM-click interventions |
| Page tool intent | Qwen via ASB | 3/8, 4/8 | planning only; not directly comparable to execution |
| Windows lifecycle | Codex via ASB | 2/2 | fresh wire/package/non-default external-effect checks |
| Windows lifecycle | Qwen via ASB | 2/2 | aligned prior evidence on the same host/model/scenario |

Qwen normalized mean on the released 60-case holdout: **75.83%**. The difference from the Codex-direct capability ceiling on the same prompts is **24.17 percentage points**.

## Holdout categories

| Category | Codex direct | Qwen→ASB run 1 | Qwen→ASB run 2 |
|---|---:|---:|---:|
| single | 10/10 | 8/10 | 8/10 |
| schema | 10/10 | 6/10 | 6/10 |
| selection | 10/10 | 9/10 | 9/10 |
| multi | 10/10 | 7/10 | 8/10 |
| recovery | 10/10 | 8/10 | 8/10 |
| safety | 10/10 | 8/10 | 6/10 |

Qwen latency:

- Run 1: mean 4.384 s; median 4.303 s; p95 5.954 s; max 7.960 s.
- Run 2: mean 4.251 s; median 4.151 s; p95 5.776 s; max 8.041 s.

## PW-CLICK-01

The previous transport/mapping failure is fixed: pw_click is present and callable, and ASB wizard forward/back controls worked.

On the frozen benchmark page, however:

- pw_click on submit/reset returned success.
- The expected page state did not change.
- Mouse click produced no effect.
- Direct DOM element click produced the expected submit/reset effects.

This is an execution-correctness issue because a human developer may accept an action that reports success and later package it into a deterministic executable.

### PASS gate

Re-run both of the following without DOM-eval fallback:

1. ASB wizard forward/back click changes the wizard step.
2. Frozen inline-handler submit/reset click changes the expected DOM state.

Both calls must return success **and** pass an observable-effect assertion. After that revalidation, the report verdict becomes PASS.

## Product-threat-model interpretation

ASB does not target an unattended autonomous-agent mode in this benchmark. AI participates during attended development; a human observes and corrects the proposed workflow before deterministic packaging.

Accordingly:

- An unsafe Qwen suggestion is a review/UI-warning concern, not evidence of autonomous production compromise.
- Qwen format variability measures correction cost and development efficiency.
- Sealed-blind isolation controls whether a score may be called a strict blind benchmark; it does not affect packaged runtime safety.
- Optional runtime AI redo or dynamic exception handling would need a separate threat model and is not claimed here.

## Reproducibility and limitations

- The public holdout and schema already exist in this repository.
- Reviewed result hashes are recorded in reviewed-summary.json; raw model responses remain unpublished per repository policy.
- Codex direct predictions were locked before expected values were loaded, but this was operator-mediated and has no comparable model latency.
- The sealed builder exposed expected data to the execution environment, so no strict sealed-blind Codex claim is made.
- Page intent and page execution are separate layers and must not be combined into one ranking score.

Repository commit at report generation: 6beb5bbb32e7d4b5fae07d99a00869d934b9e1e6
