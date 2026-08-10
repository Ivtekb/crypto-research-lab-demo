from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
BUNDLE_PATH = ROOT_DIR / "demo_data" / "demo_bundle.sqlite3"

ALLOWED_TABLES = {
    "dashboard_summary",
    "final_research_ranking",
    "run_change_report",
    "candidate_factsheets",
}

BOOLEAN_COLUMNS = {"required_manual_review"}


def _connect() -> sqlite3.Connection:
    if not BUNDLE_PATH.is_file():
        raise FileNotFoundError("The hosted demo data bundle is missing.")
    return sqlite3.connect(f"file:{BUNDLE_PATH}?mode=ro", uri=True)


def load_demo_frame(name: str) -> pd.DataFrame:
    if name not in ALLOWED_TABLES:
        raise ValueError(f"Unknown demo table: {name}")
    with _connect() as connection:
        frame = pd.read_sql_query(f'SELECT * FROM "{name}"', connection)
    for column in BOOLEAN_COLUMNS.intersection(frame.columns):
        normalized = frame[column].astype(str).str.strip().str.lower().map(
            {"1": True, "true": True, "yes": True, "0": False, "false": False, "no": False}
        )
        if normalized.notna().all():
            frame[column] = normalized.astype(bool)
    return frame


def load_demo_summary() -> dict[str, str]:
    frame = load_demo_frame("dashboard_summary")
    if frame.empty or not {"metric", "value"}.issubset(frame.columns):
        return {}
    return dict(zip(frame["metric"].astype(str), frame["value"].astype(str)))


def load_demo_metadata() -> dict[str, str]:
    with _connect() as connection:
        frame = pd.read_sql_query('SELECT key, value FROM "demo_metadata"', connection)
    if frame.empty:
        return {}
    return dict(zip(frame["key"].astype(str), frame["value"].astype(str)))
