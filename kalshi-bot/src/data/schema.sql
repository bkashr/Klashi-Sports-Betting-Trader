CREATE TABLE IF NOT EXISTS games (
  game_id TEXT PRIMARY KEY,
  sport TEXT NOT NULL,
  league TEXT,
  home_team TEXT,
  away_team TEXT,
  start_time_utc TEXT,
  pregame_spread REAL,
  pregame_total REAL,
  status TEXT,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_map (
  game_id TEXT NOT NULL,
  kalshi_ticker TEXT NOT NULL,
  market_type TEXT NOT NULL,
  line_value REAL NOT NULL,
  side_convention_json TEXT NOT NULL,
  PRIMARY KEY (game_id, kalshi_ticker)
);

CREATE TABLE IF NOT EXISTS orderbook_ticks (
  ts TEXT NOT NULL,
  kalshi_ticker TEXT NOT NULL,
  best_yes_bid INTEGER,
  best_yes_ask INTEGER,
  best_no_bid INTEGER,
  best_no_ask INTEGER,
  mid_yes REAL,
  spread_yes INTEGER,
  depth_yes_top INTEGER,
  depth_no_top INTEGER
);

CREATE TABLE IF NOT EXISTS game_state_ticks (
  ts TEXT NOT NULL,
  game_id TEXT NOT NULL,
  payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS signals (
  ts TEXT NOT NULL,
  game_id TEXT NOT NULL,
  kalshi_ticker TEXT NOT NULL,
  strategy_name TEXT NOT NULL,
  signal_strength REAL,
  direction TEXT,
  fair_prob REAL,
  market_prob REAL,
  edge REAL,
  reason_code TEXT NOT NULL,
  features_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
  order_id TEXT PRIMARY KEY,
  kalshi_order_id TEXT,
  ts_submitted TEXT NOT NULL,
  kalshi_ticker TEXT NOT NULL,
  side TEXT NOT NULL,
  action TEXT NOT NULL,
  price_cents INTEGER NOT NULL,
  contracts INTEGER NOT NULL,
  status TEXT NOT NULL,
  mode TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fills (
  ts_fill TEXT NOT NULL,
  order_id TEXT NOT NULL,
  fill_price_cents INTEGER NOT NULL,
  fill_contracts INTEGER NOT NULL,
  fees_cents INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS positions (
  kalshi_ticker TEXT PRIMARY KEY,
  net_contracts_yes INTEGER DEFAULT 0,
  avg_price_yes REAL DEFAULT 0,
  net_contracts_no INTEGER DEFAULT 0,
  avg_price_no REAL DEFAULT 0,
  unrealized_pnl REAL DEFAULT 0,
  realized_pnl REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pnl (
  ts TEXT NOT NULL,
  scope TEXT NOT NULL,
  scope_id TEXT,
  realized_usd REAL DEFAULT 0,
  unrealized_usd REAL DEFAULT 0
);
