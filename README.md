# ASB Model Eval

A reproducible evaluation harness for testing local and cloud language models against Automation Skill Builder (ASB) tool-calling conventions, typed parameters, recovery behavior and safety gates.

This is an ASB-oriented synthetic benchmark, not a third-party production gold standard. Mock success measures model planning only; it does not prove that a desktop action, parameterized skill or packaged executable worked.

## Related projects

- Targeted model: https://huggingface.co/weahoo/ASB-Qwen2.5-Coder-7B-Targeted-v2-GGUF
- Automation Skill Builder: https://www.visualbuild.me/

## Included evaluations

| Set | Cases | Purpose |
|---|---:|---|
| development_v1 | 40 | Diagnostic set; its failure categories later informed training |
| holdout_v1 | 60 | Post-training cases with new paths, values and wording |
| Live ASB | Reports | UI configuration, parameter analysis, wiring, packaging and executable validation |

## Quick start

Windows:

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    copy configs\ollama.example.yaml configs\local.yaml

macOS/Linux:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp configs/ollama.example.yaml configs/local.yaml

Edit the model ID in configs/local.yaml, then run:

    python runners/run_openai_compatible.py --config configs/local.yaml --cases benchmarks/holdout_v1.jsonl --tools schemas/asb_mock_tools.json --output results/holdout.json
    python scoring/score_results.py --cases benchmarks/holdout_v1.jsonl --results results/holdout.json --tools schemas/asb_mock_tools.json --output results/holdout.score.json

Raw files under results/ are intentionally ignored. Publish only reviewed, redacted reports.

## Ollama setup

Download/run from Hugging Face:

    ollama run hf.co/weahoo/ASB-Qwen2.5-Coder-7B-Targeted-v2-GGUF:Q4_K_M

For a local GGUF, create a named model with a Qwen2.5 tools-aware chat template. A generic Prompt-only template may cause correct tool calls to appear as JSON in message.content instead of native message.tool_calls.

Example parameters:

    FROM ./ASB-Qwen2.5-Coder-7B-Targeted-v2-Q4_K_M.gguf
    PARAMETER temperature 0.1
    PARAMETER top_p 0.9
    PARAMETER num_ctx 32768

Do not infer usable context from PARAMETER num_ctx alone. Check the GGUF metadata:

    ollama show asb-qwen25-coder-targeted-v2 --verbose

The evaluated Q4_K_M file reports:

    qwen2.context_length = 32768

Setting num_ctx 49152 did not override that model metadata. The tested ASB Start describing request was about 37.3k tokens and was rejected before inference. A truly long-context GGUF/export or a smaller ASB tool prompt is required for that route.

## Current targeted-v2 finding

Windows/Ollama evaluation on 2026-08-28 found:

| Capability | Result |
|---|---|
| Semantic smoke behavior | 3/3 correct |
| Leading-zero string preservation | Pass |
| Destructive-request refusal | Pass |
| Native OpenAI-compatible tool_calls | Fail; calls appeared in content JSON |
| Short code generation | Failed source review after two attempts |
| ASB parameter analysis | Pass; 3/3 inputs plus output |
| Model-wiring preview | Pass after deterministic code correction |
| Windows EXE packaging | Pass |
| Two non-default EXE runs | Pass |
| Independent trusted-agent lifecycle | Not achieved |

The successful EXE proves the ASB wiring and packaging path. It does not prove independent model completion because generated code required deterministic correction.

See reports/2026-08-28-qwen25-targeted-v2-asb-lifecycle.md for evidence and limitations.

## Layered evaluation framework

Model quality, ASB platform capability, and autonomous lifecycle completion are reported separately. A capable external operator driving the normal ASB UI establishes the **Expert ASB Baseline**; it is an oracle ceiling, not a model score. Offline models are then evaluated directly, through the ASB API, and through the autonomous UI lifecycle.

The framework defines autonomy gap, interface loss, fine-tuning gain, quantization loss, lifecycle gates, controlled conditions, and the comparison matrix for Qwen, Ministral, and IBM Granite.

See [docs/layered-evaluation.md](docs/layered-evaluation.md).

## Codex + ASB strong-agent ceiling

A fixed 20-case EvalPlus pilot (10 HumanEval+ and 10 MBPP+) measured a strong external agent authoring solutions and using ASB run_code as the official execution surface.

| Metric | Result |
|---|---:|
| First-attempt HumanEval+ | 9/10 |
| First-attempt MBPP+ | 8/10 |
| Combined first attempt | 17/20 (85%) |
| Retry-1 corrections | 3/3 |
| Cumulative solved | 20/20 (100%) |
| ASB execution results returned | 20/20 |
| Lost or fabricated results | 0 |
| Representative packaged runs | 3/3 |

Within this fixed pilot, no additional correctness loss attributable to ASB was observed. The three initial failures were solution errors and passed after one explicit retry. Three representative operations also passed model-wiring preview, Windows EXE packaging, non-default inputs, and external JSON verification.

This is a Codex + ASB platform ceiling, not a Qwen/Granite/Mistral model score and not a full EvalPlus leaderboard result. An entirely ASB-free replay was not independently executed on the same host, so the evidence supports “no observed ASB-induced loss in this pilot,” not universal equivalence.

- [Reviewed report](results/2026-08-28-codex-asb-evalplus-pilot.md)
- [Machine-readable summary](results/2026-08-28-codex-asb-evalplus-pilot.json)

## Honest interpretation

Development scores are useful for debugging but are not independent evidence after their failures influence training. Report holdout results separately.

A real ASB lifecycle pass requires correct parameter analysis, wire-preview success without deleting inputs, successful packaging, execution with non-default parameters, and verification of external effects rather than only exit code zero.

See docs/methodology.md, docs/metrics.md, and reports/README.md.

## Evaluation layers (v0.2)

Public development, released holdout, public lifecycle cases, official adapter registry, and a commitment to the active sealed suite are included. Lifecycle passes require a real package and two non-default external-effect checks. See docs/benchmark-publication-policy.md.
