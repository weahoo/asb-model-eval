# Codex + ASB EvalPlus pilot

Date: 2026-08-28
Scope: deterministic 10 HumanEval+ + 10 MBPP+ subset
Selection seed: asb-codex-peak-v1
Execution: Codex-authored solutions → ASBNGROK run_code → Windows WSL Ubuntu → EvalPlus 0.3.1

This is a fixed-sample pilot, not a full EvalPlus leaderboard score.

## Results

| Metric | Result |
|---|---:|
| HumanEval+ first attempt | 9/10 |
| MBPP+ first attempt | 8/10 |
| Combined first attempt | 17/20 (85%) |
| Retry-1 failed cases | 3/3 |
| Cumulative solved | 20/20 (100%) |
| ASB transport/execution completion | 20/20 |
| Lost or fabricated results | 0 |

The three initial failures were solution errors. All were corrected without reading canonical solutions. ASB returned every official base/plus status.

## Environment observations

- EvalPlus 0.3.1 installs on native Windows but its evaluator imports Unix resource; native evaluation is unsupported.
- WSL Ubuntu was used for official EvalPlus execution semantics.
- The EvalPlus CLI requires complete dataset coverage. This pilot used EvalPlus get_groundtruth and check_correctness directly for the frozen subset.
- HumanEval+ v0.1.10 and MBPP+ v0.2.0 cache files were reused after SHA-256 verification.
- BFCL was deferred because its official Windows CLI dependency set is disproportionately heavy for this machine.

## ASB packaging lifecycle

A three-operation runner covered decimal-digit sum encoded as binary, parenthesis-group separation, and maximum-sum increasing subsequence with a later required element.

Parameter analysis was submitted but blocked before inference because Settings referenced missing model asb-qwen25-coder-targeted-v2:latest. Codex supplied the deterministic schema as an expert recovery.

| Gate | Result |
|---|---|
| Inputs retained | 3/3 |
| Wiring mode | model |
| ai_sk_wire_preview | ok=true |
| Wiring issues | none |
| Windows EXE ZIP | created |
| Non-default executions | 3/3 |
| Exit codes | 3/3 zero |
| External JSON artifacts | 3/3 verified |

Artifact:
E:\Test\project\project\skill_exe_builds\codex_asb_benchmark_runner-Windows.zip

Size: 6,896,412 bytes
SHA-256: a8fa37de40114d6b46c30561fb0268e4d836b56354684016cef536407abf6beb

## Interpretation

The observed coding score was 85% at first attempt and 100% after one explicit retry. ASB run_code completed and returned all 20 evaluations, so no correctness loss was attributed to ASB in this pilot. The assetization path produced a real Windows package and passed three non-default external-effect checks.

A completely ASB-free replay was not independently executed on the same Windows/WSL host; this report therefore does not claim an empirical direct-vs-ASB delta of zero. It establishes the Codex + ASB strong-agent result and ASB execution/packaging completion.
