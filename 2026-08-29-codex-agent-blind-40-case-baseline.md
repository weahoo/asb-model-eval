# Codex agent blind baseline — ASB 40-case mock suite

Date: 2026-08-29

## Outcome

| Runner / model | Overall | Tool cases | Safety | API latency |
|---|---:|---:|---:|---:|
| Codex agent blind/manual baseline | **97.5%** | **97.22%** | **100%** | N/A |
| Qwen3-8B tool-call Pilot v1, L4/Ollama | 75% | 72.22% | 100% | 6.64 s |
| Qwen 3.5 local baseline | 75% | 75% | 75% | 19.39 s |
| Granite 4.2 targeted-v1 | 70% | 66.67% | 100% | 64.77 s |
| Qwen2.5-Coder targeted-v2 | 10% | 0% | 100% | 8.54 s |

Qwen2.5 targeted-v2's zero tool-case rate reflects its OpenAI-compatible protocol problem: calls were emitted in message content instead of native message.tool_calls.

## Blind-test method

Before answering, the evaluator exposed only:

- case ID, category, and user prompt;
- tool names and JSON schemas.

The expected object was withheld until all 40 predictions had been written. The existing score_results.py then scored first-tool selection, argument subsets, and safety refusal.

This is an **agent capability ceiling**, not an API throughput benchmark. Codex was not invoked through the same Ollama/OpenAI-compatible endpoint, so the scorer's synthetic HTTP-success and zero-latency fields must not be compared with local models. Only task accuracy, schema decisions, and safety are comparable.

## Failure

Only M29 failed.

- Requested first action: back up data.txt as data.bak.
- Selected tool: data_copy — correct.
- Submitted arguments: data.txt → data.bak.
- Hidden expected context: tmp/model_eval/data.txt → tmp/model_eval/data.bak.
- Classification: correct tool, incorrect inherited path context.

## Category results

| Category | Passed |
|---|---:|
| Single tool | 10/10 |
| Schema | 7/7 |
| Tool selection | 3/3 |
| Multi-step first action | 9/10 |
| Recovery | 6/6 |
| Safety | 4/4 |
| Total | 39/40 |

## Interpretation

The result does not support claiming a 100% Codex score. It establishes a 97.5% blind first-action baseline on this compact mock suite. It also shows that ASB itself does not inherently force a large accuracy loss: a stronger external agent can map the same schemas reliably. The remaining gap for local models is primarily model/tool-protocol and reasoning quality, not the basic ASB tool definitions.

A stricter next comparison should add real execution, tool-result turns, run_code repair, wiring preview, EXE packaging, and non-default parameter verification.
