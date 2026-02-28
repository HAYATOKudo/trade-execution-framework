# Architecture

This repository is a **public execution framework skeleton** designed for production-style integrations.
It intentionally excludes any proprietary trading strategy, AI training, parameters, or performance logs.

## Goals
- Demonstrate **clean layering** and maintainable structure
- Provide runnable examples and safe defaults (no secrets committed)
- Keep dependencies minimal for portability

## Layers
### infra/
Responsible for talking to external services (HTTP/API). No business decisions.

### execution/
Order / workflow management. Retries, idempotency hooks, and orchestration live here.

### llm/
Provider interface + a mock provider for demos. Optional OpenAI provider is included as an integration example.

### strategy/
Public stub only. Real strategies belong in a private repo.

## Safety & hygiene
- .env is ignored; .env.example documents required variables
- logs/db/data are excluded by .gitignore
- public examples never include keys or performance numbers

## Why this structure
Clients pay for **reliable integration**: clear boundaries, testability, and safe operations.
