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
