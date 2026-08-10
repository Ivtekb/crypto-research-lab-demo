from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_SOURCE = (ROOT / "app" / "streamlit_app.py").read_text()
LOADER_SOURCE = (ROOT / "app" / "demo_loader.py").read_text()
BUNDLE_PATH = ROOT / "demo_data" / "demo_bundle.sqlite3"

EXPECTED_TABLES = {
    "dashboard_summary",
    "final_research_ranking",
    "run_change_report",
    "candidate_factsheets",
    "demo_metadata",
}

FORBIDDEN_COLUMNS = {
    "cg_id",
    "manual_review_status",
    "eligible_for_scoring",
    "final_candidate_status",
    "data_quality_flags",
    "unlock_data_available",
    "next_unlock_date",
    "next_unlock_pct_market_cap",
}


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(f"file:{BUNDLE_PATH}?mode=ro", uri=True)


def test_demo_bundle_has_only_allowed_tables():
    with _connect() as connection:
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
    assert tables == EXPECTED_TABLES


def test_demo_bundle_has_no_forbidden_columns():
    with _connect() as connection:
        for table in EXPECTED_TABLES:
            columns = {row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')}
            assert not columns.intersection(FORBIDDEN_COLUMNS)


def test_demo_tables_keep_every_visible_candidate():
    with _connect() as connection:
        ranking_rows = connection.execute('SELECT COUNT(*) FROM "final_research_ranking"').fetchone()[0]
        factsheet_rows = connection.execute('SELECT COUNT(*) FROM "candidate_factsheets"').fetchone()[0]
        change_rows = connection.execute('SELECT COUNT(*) FROM "run_change_report"').fetchone()[0]
        summary_rows = dict(connection.execute('SELECT metric, value FROM "dashboard_summary"'))
    assert ranking_rows == int(summary_rows["final_ranking_rows"])
    assert factsheet_rows == ranking_rows
    assert change_rows == ranking_rows


def test_demo_loader_restores_boolean_display_type():
    sys.path.insert(0, str(ROOT / "app"))
    try:
        from demo_loader import load_demo_frame

        ranking = load_demo_frame("final_research_ranking")
    finally:
        sys.path.pop(0)
    assert set(ranking["required_manual_review"].map(str)) <= {"True", "False"}


def test_demo_app_has_no_pipeline_or_file_export_access():
    forbidden = [
        "subprocess",
        "run_full_pipeline",
        "run.lock",
        "manual_overrides",
        "download_button",
        "outputs/",
        ".csv",
        ".xlsx",
        "api_clients",
        "requests",
    ]
    assert not any(term in APP_SOURCE for term in forbidden)


def test_loader_is_read_only_and_table_limited():
    assert "mode=ro" in LOADER_SOURCE
    assert "ALLOWED_TABLES" in LOADER_SOURCE
    assert "INSERT" not in LOADER_SOURCE
    assert "UPDATE " not in LOADER_SOURCE
    assert "DELETE " not in LOADER_SOURCE


def test_demo_keeps_four_dashboard_tabs():
    assert 'st.tabs(["Main Cockpit", "Asymmetry Table", "Candidate Card", "What Changed"])' in APP_SOURCE


def test_demo_keeps_signal_glossary():
    assert 'st.expander("Signal Glossary", expanded=False)' in APP_SOURCE
    for section in [
        "How to use this dashboard",
        "How to read x3 / x5 / x10",
        "What data goes into the model",
        "Base vs adjusted probability",
        "Research Score",
        "Review Required",
        "Limitations",
    ]:
        assert section in APP_SOURCE


def test_demo_has_no_full_update_button():
    assert "Run full update now" not in APP_SOURCE
    assert "Pipeline Update" not in APP_SOURCE


def test_demo_hides_dataframe_csv_download():
    assert 'button[aria-label="Download as CSV"]' in APP_SOURCE
    assert "display: none !important" in APP_SOURCE
