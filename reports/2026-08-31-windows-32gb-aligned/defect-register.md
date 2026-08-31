# Reviewed defect and observation register

| ID | Class | Severity under attended mode | Status | Acceptance |
|---|---|---:|---|---|
| PW-CLICK-01 | Product execution correctness | — | CLOSED / PASS | 4/4 observable-effect checks passed through pw_click DOM backup; no external pw_eval |
| QWEN-FMT-01 | Model quality / correction cost | P2, non-blocking | OPEN | Stable single native tool call, schema-correct arguments |
| QWEN-SAFE-01 | Design-time review quality | P3, non-blocking | OPEN | Clear review warning/redaction for sensitive write/send/delete actions |
| EVAL-BLIND-01 | Benchmark governance | Non-product | OPEN | Prediction locked before isolated scorer loads expected data |
| PKG-MSG-01 | Packaging localization | P3 | OPEN | Windows build returns a Windows-specific success message key |
| MCP-DISC-01 | Discovery | — | PASS | 222 tools, including 40 direct Playwright tools |
| PW-RELAY-01 | Relay/CDP | — | PASS | Healthy relay, real CDP attachment and readable snapshot |
| LIFE-01 | Deterministic lifecycle | — | PASS | Wiring, packaging and two non-default external effects verified |
