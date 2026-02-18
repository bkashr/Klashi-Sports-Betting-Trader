# Kalshi Sports Betting Trader (V1)

Milestones 1-3 implementation:
- DB + schema + repositories
- Kalshi orderbook ingest (WS abstraction with mock stream)
- Sports feed interface + mock provider
- NBA and Soccer signal generation with reason codes
- Risk manager veto plumbing
- Orchestrator shadow mode loop (signals-only)

## Quickstart

```bash
cd kalshi-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --config config/settings.yaml
```

## Notes
- V1 runs in `shadow` mode by default (`shadow_mode: true`) and produces signals only.
- Secrets belong in `config/secrets.env` (not committed).
<<<<<<< codex/build-automated-kalshi-trading-system-8yrxs3


## Current dependency posture

- Shadow mode currently runs with Python stdlib only.
- The `requirements.txt` is intentionally empty for Milestones 1-3 in this environment.
- For later milestones (real HTTP/WS auth/signing), expect to add packages such as `requests`, `websockets`, and `cryptography`.

## Test discovery sanity check

This repository includes `kalshi-bot/tests/test_soccer_poisson.py` and a layout test that fails if that file is moved/misnamed.
Run:

```bash
cd kalshi-bot
PYTHONPATH=. python -m unittest discover -s tests -v
```
=======
>>>>>>> main
