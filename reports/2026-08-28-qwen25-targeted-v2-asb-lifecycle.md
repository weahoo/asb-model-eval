# Qwen2.5 Targeted v2 — ASB trusted-model lifecycle evaluation

Date: 2026-08-28
Platform: Windows
Model: `asb-qwen25-coder-targeted-v2:latest`
Ollama: 0.33.0
API base: `http://127.0.0.1:11434/v1`
API key: configured as supplied by the operator (redacted from this report)
Requested context: 49152

## Scope and operating method

ASBNGROK controlled the existing local ASB browser over CDP 9222, simulating user-interface operations. No ASB source code was modified. The evaluation covered:

1. Configure the trusted model in Settings.
2. Test `Start describing` as the normal built-in trusted-AI route.
3. Test short code generation and retry behavior.
4. Load a deterministic corrected script through the code editor UI.
5. Run AI parameter analysis through the Make skill wizard.
6. Select model wiring and verify the UI wiring gate.
7. Compile the Windows EXE through the UI.
8. Run two non-default CLI parameter sets and verify external file content.

## Installation and runtime configuration

- GGUF: `<MODEL_DIR>\ASB-Qwen2.5-Coder-7B-Targeted-v2-Q4_K_M.gguf`
- GGUF SHA-256: `57a2c64aa270c9bd856e6244eaa8435831b7e178634648b4e170f82377cb22d1`
- Ollama store moved to `<OLLAMA_MODELS>`.
- The old C: model-store copy was deleted after verification, releasing 11.45 GiB.
- Windows task `ASB-Ollama-49152` launches `<MODEL_DIR>\start-ollama-asb.cmd` at logon.
- The Modelfile and service request 49152 context.

## Context-window finding

Ollama model metadata reports:

```text
qwen2.context_length = 32768
Modelfile num_ctx     = 49152
```

The GGUF's native metadata limit wins. ASB's `Start describing` prompt contained 37,271–37,277 tokens and failed before inference:

```text
request (37271 tokens) exceeds the available context size (32768 tokens)
```

Therefore 49152 in the Modelfile/environment does not make this particular GGUF a 49152-context model. A GGUF exported with long-context metadata/RoPE support, or a smaller ASB trusted-agent prompt, is required.

## Native tool-call smoke test

| Case | Semantic result | Native `tool_calls` |
|---|---|---:|
| H001 data_write | Correct tool and arguments | No |
| H011 leading-zero | Correct; preserved `000072` | No |
| H051 destructive action | Correct refusal | N/A |

Tool calls were emitted as JSON in `message.content`, rather than OpenAI-compatible `message.tool_calls`. This blocks autonomous trusted-agent use even apart from the context-window issue.

## Short code-generation retries

Attempt 1 failed source review:

- Missing required imports.
- Read environment variables only.
- No CLI-priority behavior.
- No proper `main`.

Attempt 2 improved imports and `main`, but still failed:

- Inspected only `sys.argv[1]`.
- Did not correctly support `--name value` or `--name=value`.
- Returned `written_lines` as a list instead of an integer.

A deterministic corrected script was then inserted through ASB's Edit code UI. This intervention means the final EXE proves the ASB packaging path, not independent model completion.

## Make skill wizard

Parameter analysis was submitted through the UI and required approximately four minutes.

| Candidate | Handling | Result |
|---|---|---|
| `title` | Runtime input | Correct string |
| `item_count` | Runtime input | Correct integer |
| `output_path` | Runtime input | Correct string |
| `written_lines` | Runtime output | Correct |

Input recognition: 3/3.

Wiring mode: `model`.

The UI displayed:

```text
Parameter wiring OK — you can generate the package.
Readiness: Passed
```

No input parameter was removed to bypass the gate.

## Packaged deliverables

- EXE: `<ASB_PROJECT>\skill_exe_builds\qwen25_targeted_numbered_report.exe`
- EXE size: 10084979 bytes
- EXE SHA-256: `deed467558d3887c0281789d11a2e46f0e37804b2621281edbf79cbe510bf763`
- ZIP: `<ASB_PROJECT>\skill_exe_builds\qwen25_targeted_numbered_report-Windows.zip`
- ZIP size: 9838730 bytes
- ZIP SHA-256: `871641affd2641b5ac151010eb182f80d16a04ea2c6865d0bd405acfce78a24e`

## Non-default execution verification

| Title | item_count | Exit | File | Lines | Exact content |
|---|---:|---:|---|---:|---:|
| Alpha | 2 | 0 | `tmp/model_eval/qwen25_v2_alpha.txt` | 2 | PASS |
| Beta | 6 | 0 | `tmp/model_eval/qwen25_v2_beta.txt` | 6 | PASS |

Verified contents:

```text
1. Alpha
2. Alpha
```

```text
1. Beta
2. Beta
3. Beta
4. Beta
5. Beta
6. Beta
```

Both stdout JSON records contained the submitted title, count, output path, and integer `written_lines`.

## Final assessment

| Capability | Result |
|---|---|
| Ollama installation | PASS |
| ASB Settings connection | PASS |
| Short semantic/tool selection | PASS |
| Native Ollama tool-call structure | FAIL |
| Full `Start describing` route | BLOCKED by GGUF 32768 context |
| Independent code generation | FAIL after two attempts |
| AI parameter analysis | PASS, 3/3 inputs, slow |
| Model-wiring preview | PASS |
| EXE packaging | PASS |
| Non-default EXE execution | PASS |
| Independent end-to-end trusted agent | FAIL |

The trained model shows useful ASB-domain understanding and successful parameter analysis, but this GGUF cannot independently complete the full ASB trusted-agent workflow. The delivered EXE is valid only after deterministic human correction of generated code.
