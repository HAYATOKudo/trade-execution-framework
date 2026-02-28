# Security

## What must never be committed
- .env / API keys / secrets
- trading strategy logic or parameters
- logs containing sensitive identifiers
- performance metrics or PnL numbers

## Repo protections (recommended)
- Enable GitHub secret scanning (if available)
- Require PR reviews for changes under infra/ and execution/
- Keep proprietary code in a private repository

## Reporting
If you find a security issue, please open a GitHub issue with minimal details and mark it as security-related.
