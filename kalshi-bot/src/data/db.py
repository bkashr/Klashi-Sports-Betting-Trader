from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row

    def execute(self, sql: str, params: tuple = ()) -> None:
        self.conn.execute(sql, params)
        self.conn.commit()

    def executemany(self, sql: str, params_list: list[tuple]) -> None:
        self.conn.executemany(sql, params_list)
        self.conn.commit()

    def query(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        cur = self.conn.execute(sql, params)
        return cur.fetchall()

    def close(self) -> None:
        self.conn.close()


def init_schema(db: Database, schema_path: str) -> None:
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()
    db.conn.executescript(sql)
    db.conn.commit()
