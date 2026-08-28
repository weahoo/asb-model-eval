# Layered Evaluation: Expert Ceiling, Model Capability, and ASB Autonomy

This document defines how to compare general-purpose model capability, ASB platform capability, and end-to-end model autonomy without conflating them.

## Questions answered

A complete evaluation should answer three separate questions:

1. Can ASB complete the task when operated correctly?
2. Can the model solve the underlying code, schema, and tool-selection problem?
3. Can the model independently complete the workflow through ASB and deliver a verified artifact?

A single aggregate score cannot answer all three.

## Evaluation layers

| Layer | Driver | Primary measurement | Interpretation |
|---|---|---|---|
| Expert ASB baseline | A capable external operator using the normal ASB UI | ASB platform and workflow ceiling | Whether ASB can complete the task when correctly operated |
| Direct model benchmark | Model through the standard benchmark harness | General code, schema, reasoning, and tool-call capability | Model capability without ASB UI or packaging effects |
| ASB API integration | Model using ASB tools through an OpenAI-compatible interface | Protocol and tool-integration compatibility | Whether the model and serving stack can exchange valid tool calls |
| Autonomous ASB lifecycle | Trusted model operating the supported ASB workflow | Product-level autonomy | Whether the model can independently produce and validate the deliverable |

The expert baseline is an oracle or expert-operation ceiling. It must never be reported as an autonomous model result.

## Derived gaps

Report these differences separately:

- Autonomy gap = expert ASB success rate minus autonomous model success rate.
- UI/interface loss = ASB API integration success rate minus normal-UI lifecycle success rate.
- Fine-tuning gain = tuned-model result minus the matching untuned base-model result.
- Quantization loss = BF16/FP16 result minus the matching GGUF quantized result.
- Protocol loss = semantically correct tool intent minus native message.tool_calls success.

A model that emits the correct function and arguments as JSON inside message.content has semantic tool knowledge but has failed native OpenAI-compatible tool-call routing.

## Test matrix

Evaluate untuned and ASB-tuned variants under the same holdout:

| Model family | Untuned baseline | ASB-tuned candidate |
|---|---|---|
| Qwen2.5-Coder-7B | Official Instruct | Targeted v2 or a method-matched successor |
| Ministral 3 8B | Official Instruct | ASB v1 |
| IBM Granite 4.2 8B | Official checkpoint | ASB v1 |

Training methods must be disclosed. If one adapter supervises every assistant decision turn while another supervises only the final assistant message, the result is not a pure base-model comparison.

## Benchmark groups

### Standard model benchmarks

Use official or widely accepted harnesses where practical:

- HumanEval and MBPP for code generation.
- BFCL-style cases for function calling.
- JSON/schema validation for structured output.
- Multilingual prompts, including Chinese input with English tool names.
- Long-context acceptance and retrieval at context sizes used by ASB.

Results produced through a modified ASB UI flow must not be presented as directly comparable to official leaderboard scores.

### ASB planning benchmark

Use the locked mock/holdout cases in this repository to measure:

- first-tool selection;
- native message.tool_calls;
- valid arguments JSON;
- schema and type compliance;
- multi-turn continuation after a tool result;
- failure recovery;
- safety refusal;
- hallucinated-success rate;
- latency and tool rounds.

Mock success measures planning and protocol behavior only. It does not prove that a desktop action or packaged executable worked.

### Live ASB lifecycle benchmark

Use the normal user-visible ASB workflow. Representative coverage should include:

- trusted-model configuration;
- code generation or user-action recording;
- parameter analysis;
- model-wiring and app-wiring selection;
- ai_sk_wire_preview;
- correction and re-analysis after a failed preview;
- packaging;
- execution with non-default parameters;
- verification of stdout, response JSON, and external effects.

For a packaged skill, exit code zero alone is insufficient.

## Lifecycle success gate

A lifecycle case passes only when all required gates pass:

1. Required business parameters are present and correctly typed.
2. No parameter is removed merely to bypass wiring validation.
3. Wiring preview returns ok: true with no unresolved issues.
4. Packaging produces the expected platform artifact.
5. The artifact runs with values different from recorded/default values.
6. Observable output matches those new values.
7. Tool or MCP failure count is zero where applicable.
8. No external operator edits model output or chooses a recovery step during an autonomous run.

If an operator repairs code or parameters, record the case as assisted completion, not autonomous success.

## Execution modes

Keep these modes distinct in raw results and reports:

| Mode | Description |
|---|---|
| expert_ui | External expert simulates normal human operation through the ASB UI |
| model_direct | Model runs a standard benchmark without ASB |
| model_asb_api | Model selects and calls ASB tools through the API |
| model_asb_ui | Trusted model completes the supported UI lifecycle |
| assisted_asb_ui | Model starts the lifecycle but an external operator intervenes |

Do not merge assisted_asb_ui with model_asb_ui.

## Controlled conditions

For comparisons, hold constant:

- hardware and operating system;
- serving software and version;
- quantization;
- context size;
- chat template and tool parser;
- tool catalog;
- maximum action/tool budget;
- temperature, top-p, and thinking mode;
- timeouts;
- benchmark revision;
- scoring revision.

Run each case at least twice. Run release-critical lifecycle cases three times to expose output instability.

For reasoning models, report non-thinking, low-effort, and full-thinking modes separately when supported.

## Minimum reported metrics

- Task success rate.
- Native tool-call rate.
- First-tool accuracy.
- Schema pass rate.
- Argument/type accuracy.
- Multi-turn continuation rate.
- Recovery success rate.
- Safety refusal rate.
- Hallucinated-success rate.
- Parameter-analysis completeness.
- Wiring-preview pass rate.
- Package success rate.
- Non-default artifact validation rate.
- Mean and percentile latency.
- Peak memory where available.
- Average tool rounds.

## Holdout integrity

The public diagnostic set may guide development. Once its failures influence training, it is no longer independent evidence.

Use a locked holdout with:

- prompts absent from training;
- new paths, names, values, and failure branches;
- no exact or templated leakage;
- immutable case IDs and expected outcomes;
- a recorded dataset and scorer hash.

Training loss and validation loss are diagnostics, but neither substitutes for the locked behavioral holdout.

## Reporting

A public comparison should contain three scorecards rather than one blended number:

1. General capability.
2. ASB planning and protocol.
3. Verified autonomous lifecycle.

The recommended headline is the verified autonomous lifecycle rate, accompanied by the expert ceiling and autonomy gap.

Example:

| Result | Rate |
|---|---:|
| Expert ASB baseline | 95% |
| Granite autonomous lifecycle | 82% |
| Ministral autonomous lifecycle | 75% |
| Qwen autonomous lifecycle | 60% |

In this example, Granite's autonomy gap is 13 percentage points. The expert result demonstrates the platform ceiling; it does not claim that the model independently achieved 95%.
