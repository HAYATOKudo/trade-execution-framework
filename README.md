# trade-execution-framework

Public, safety-first skeleton for a maker-style trade execution system.

## What this repo includes
- Infra layer: signed API client (GET/POST skeleton)
- Execution layer: maker order management (quote/cancel/replace)
- Live loop skeleton
- Logging & config structure
- Strategy stub (NO strategy logic is published)

## What this repo does NOT include (by design)
- Any proprietary strategy logic
- Any AI training code / parameters
- Any performance logs / PnL numbers
- Any API keys or secrets

## Quick start
1) Copy .env.example to .env and fill your own keys (never commit .env)
2) Run the live loop skeleton (stub strategy will always return NO_TRADE)

## Contact / communication
I’m hearing-impaired, so I rely on chat for technical discussions. I’m happy to join video calls.
