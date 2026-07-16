from __future__ import annotations

from typing import Iterable

import pandas as pd
import streamlit as st

from demo_loader import load_demo_frame, load_demo_metadata, load_demo_summary

SIGNAL_COLUMNS = [
    "final_rank",
    "symbol",
    "name",
    "sector",
    "research_priority_score",
    "x3_probability_emissions_adjusted_pct",
    "x5_probability_emissions_adjusted_pct",
    "x10_probability_emissions_adjusted_pct",
    "emissions_risk_bucket",
    "required_manual_review",
    "manual_review_reasons",
    "top_positive_signal",
    "top_risk_signal",
]

ASYMMETRY_COLUMNS = [
    "final_rank",
    "symbol",
    "name",
    "sector",
    "functional_category",
    "research_priority_score",
    "research_priority_tier",
    "x3_probability_emissions_adjusted_pct",
    "x5_probability_emissions_adjusted_pct",
    "x10_probability_emissions_adjusted_pct",
    "probability_confidence",
    "emissions_adjusted_confidence",
    "emissions_risk_bucket",
    "emissions_adjustment_reason",
    "required_manual_review",
    "manual_review_reasons",
    "top_positive_signal",
    "top_risk_signal",
]

CHANGE_COLUMNS = [
    "symbol",
    "name",
    "previous_rank",
    "current_rank",
    "rank_change",
    "previous_x10_probability_pct",
    "current_x10_probability_pct",
    "previous_adjusted_x10_probability_pct",
    "current_adjusted_x10_probability_pct",
    "previous_research_priority_score",
    "current_research_priority_score",
    "status_change",
    "change_reason",
]

DISPLAY_LABELS = {
    "v1_0_status": "Run Status",
    "clean_candidate_count": "Clean Candidates",
    "final_ranking_rows": "Final Ranking Rows",
    "manual_qa_required_count": "Manual Review Count",
    "missing_unlock_data_count": "Missing Unlock Data",
    "calibration_status": "Calibration Status",
    "calculated_return_rows": "Calculated Return Rows",
    "not_matured_return_rows": "Not Matured Return Rows",
    "final_rank": "Rank",
    "symbol": "Asset",
    "name": "Name",
    "sector": "Sector",
    "functional_category": "Category",
    "research_priority_score": "Research Score",
    "research_priority_tier": "Research Tier",
    "x3_probability_pct": "Base x3 Signal",
    "x5_probability_pct": "Base x5 Signal",
    "x10_probability_pct": "Base x10 Signal",
    "x3_probability_emissions_adjusted_pct": "Adj. x3 Signal",
    "x5_probability_emissions_adjusted_pct": "Adj. x5 Signal",
    "x10_probability_emissions_adjusted_pct": "Adj. x10 Signal",
    "probability_confidence": "Signal Confidence",
    "emissions_adjusted_confidence": "Adjusted Confidence",
    "emissions_risk_bucket": "Dilution / Emissions Risk",
    "emissions_adjustment_reason": "Adjustment Reason",
    "required_manual_review": "Review Required",
    "manual_review_reasons": "Review Flags",
    "top_positive_signal": "Why It Ranked",
    "top_risk_signal": "Main Risk",
    "current_rank": "Current Rank",
    "previous_rank": "Previous Rank",
    "rank_change": "Rank Movement",
    "status_change": "Change Status",
    "change_reason": "Change Reason",
    "market_cap_usd": "Market Cap",
    "fdv_usd": "FDV",
    "tvl_usd": "TVL",
    "revenue_30d_usd": "30D Revenue",
    "fees_30d_usd": "30D Fees",
    "fundamental_score": "Fundamental Score",
    "sector_relative_value_score": "Sector-Relative Value Score",
    "unlock_data_status": "Unlock Data Status",
    "historical_return_status": "Historical Return Status",
    "base_x3_probability_pct": "Base x3 Signal",
    "base_x5_probability_pct": "Base x5 Signal",
    "base_x10_probability_pct": "Base x10 Signal",
    "adjusted_x3_probability_pct": "Adj. x3 Signal",
    "adjusted_x5_probability_pct": "Adj. x5 Signal",
    "adjusted_x10_probability_pct": "Adj. x10 Signal",
    "previous_x10_probability_pct": "Previous x10 Signal",
    "current_x10_probability_pct": "Current x10 Signal",
    "previous_adjusted_x10_probability_pct": "Previous Adj. x10 Signal",
    "current_adjusted_x10_probability_pct": "Current Adj. x10 Signal",
    "previous_research_priority_score": "Previous Research Score",
    "current_research_priority_score": "Current Research Score",
}

SUMMARY_VALUE_LABELS = {
    "production_mvp_ready_with_data_gaps": "Ready, with data gaps",
    "production_mvp_ready": "Ready",
    "needs_fix": "Needs fix",
    "insufficient_history": "Insufficient history",
}

MISSING_VALUE_LABEL = "Not available"

PERCENT_COLUMNS = {
    "x3_probability_pct",
    "x5_probability_pct",
    "x10_probability_pct",
    "x3_probability_emissions_adjusted_pct",
    "x5_probability_emissions_adjusted_pct",
    "x10_probability_emissions_adjusted_pct",
    "base_x3_probability_pct",
    "base_x5_probability_pct",
    "base_x10_probability_pct",
    "adjusted_x3_probability_pct",
    "adjusted_x5_probability_pct",
    "adjusted_x10_probability_pct",
    "previous_x10_probability_pct",
    "current_x10_probability_pct",
    "previous_adjusted_x10_probability_pct",
    "current_adjusted_x10_probability_pct",
}

USD_COLUMNS = {
    "market_cap_usd",
    "fdv_usd",
    "tvl_usd",
    "revenue_30d_usd",
    "fees_30d_usd",
}

ONE_DECIMAL_COLUMNS = {
    "research_priority_score",
    "previous_research_priority_score",
    "current_research_priority_score",
    "fundamental_score",
    "sector_relative_value_score",
}

INTEGER_COLUMNS = {
    "final_rank",
    "previous_rank",
    "current_rank",
}

CONTROLLED_TEXT_COLUMNS = {
    "emissions_risk_bucket",
    "dilution_risk_bucket",
    "probability_confidence",
    "emissions_adjusted_confidence",
    "research_priority_tier",
    "status_change",
    "change_reason",
    "top_positive_signal",
    "top_risk_signal",
    "unlock_data_status",
    "historical_return_status",
    "calibration_status",
    "emissions_adjustment_reason",
}

REVIEW_FLAG_LABELS = {
    "missing_unlock_data": "Missing unlock schedule",
    "insufficient_historical_calibration": "Not enough historical calibration",
    "missing_cg_id": "Missing CoinGecko ID",
    "token_unlock_qa_required": "Unlock data requires QA",
}

INFO_CARDS = [
    (
        "How to use this dashboard",
        "Start with the top x10, x5, and x3 tables. Then check Why It Ranked, Main Risk, and Review Flags before opening the Candidate Card.",
    ),
    (
        "How to read x3 / x5 / x10",
        "These are research signals, not predictions. Higher means the asset looks more worth reviewing for that upside case. x10 is the most uncertain.",
    ),
    (
        "What data goes into the model",
        "It combines market size, liquidity, TVL, fees, revenue, valuation, token supply risk, unlock data, and data quality flags.",
    ),
    (
        "Base vs adjusted probability",
        "Base is the raw model signal. Adjusted applies a supply-risk haircut for dilution, FDV overhang, emissions risk, and missing unlock data.",
    ),
    (
        "Research Score",
        "A 0-100 queue score. Higher means review earlier. It combines adjusted x3/x5/x10 signals, fundamentals, valuation, and confidence.",
    ),
    (
        "Review Required",
        "Yes means the asset has a data gap or risk flag. It is not a bad label; it means a human should verify the signal.",
    ),
    (
        "Limitations",
        "Public data can change, unlock data may be missing, history may be immature, and qualitative risks are not fully captured. No recommendations or price targets.",
    ),
]


def _existing_columns(df: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    return [column for column in columns if column in df.columns]


def _coerce_bool_options(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().map({"true": True, "false": False}).fillna(series)


def display_label(field: str) -> str:
    return DISPLAY_LABELS.get(field, field.replace("_", " ").title())


def format_display_value(value: object) -> object:
    if pd.isna(value):
        return MISSING_VALUE_LABEL
    if isinstance(value, bool):
        return "Yes" if value else "No"
    text = str(value)
    if text in {"True", "False"}:
        return "Yes" if text == "True" else "No"
    if text.strip() == "" or text.lower() in {"nan", "none", "<na>"}:
        return MISSING_VALUE_LABEL
    return SUMMARY_VALUE_LABELS.get(text, text.replace("_", " "))


def format_compact_usd(value: object) -> str:
    number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(number):
        return MISSING_VALUE_LABEL
    sign = "-" if number < 0 else ""
    number = abs(float(number))
    if number >= 1_000_000_000:
        return f"{sign}${number / 1_000_000_000:.1f}B"
    if number >= 1_000_000:
        return f"{sign}${number / 1_000_000:.1f}M"
    if number >= 1_000:
        return f"{sign}${number / 1_000:.1f}K"
    return f"{sign}${number:.0f}"


def format_percent(value: object) -> str:
    number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(number):
        return MISSING_VALUE_LABEL
    return f"{float(number):.1f}%"


def format_one_decimal(value: object) -> str:
    number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(number):
        return MISSING_VALUE_LABEL
    return f"{float(number):.1f}"


def format_integer(value: object) -> str:
    number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(number):
        return MISSING_VALUE_LABEL
    return f"{int(number)}"


def format_rank_movement(value: object) -> str:
    number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(number):
        return MISSING_VALUE_LABEL
    number = float(number)
    if number > 0:
        return f"+{int(number) if number.is_integer() else round(number, 1)}"
    if number < 0:
        return f"{int(number) if number.is_integer() else round(number, 1)}"
    return "0"


def format_readable_text(value: object) -> str:
    formatted = format_display_value(value)
    if formatted == MISSING_VALUE_LABEL:
        return formatted
    return str(formatted).replace("_", " ").title()


def format_review_flags(value: object) -> object:
    if pd.isna(value):
        return MISSING_VALUE_LABEL
    flags = [item.strip() for item in str(value).split(";") if item.strip()]
    if not flags:
        return MISSING_VALUE_LABEL
    return "; ".join(REVIEW_FLAG_LABELS.get(flag, flag.replace("_", " ")) for flag in flags)


def display_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for column in out.columns:
        if column == "manual_review_reasons":
            out[column] = out[column].map(format_review_flags)
        elif column in PERCENT_COLUMNS:
            out[column] = out[column].map(format_percent)
        elif column in USD_COLUMNS:
            out[column] = out[column].map(format_compact_usd)
        elif column in ONE_DECIMAL_COLUMNS:
            out[column] = out[column].map(format_one_decimal)
        elif column in INTEGER_COLUMNS:
            out[column] = out[column].map(format_integer)
        elif column == "rank_change":
            out[column] = out[column].map(format_rank_movement)
        elif column == "required_manual_review":
            out[column] = out[column].map(format_display_value)
        elif column in CONTROLLED_TEXT_COLUMNS:
            out[column] = out[column].map(format_readable_text)
        elif out[column].dtype == "object" or out[column].dtype == "bool":
            out[column] = out[column].map(format_display_value)
    return out.rename(columns={column: display_label(column) for column in out.columns})


def display_cell_value(column: str, value: object) -> object:
    if column == "manual_review_reasons":
        return format_review_flags(value)
    return display_dataframe(pd.DataFrame([{column: value}])).iloc[0, 0]


def render_metric_group(row: pd.Series, fields: list[str], columns_per_row: int = 3) -> None:
    visible_fields = [field for field in fields if field in row.index]
    for start in range(0, len(visible_fields), columns_per_row):
        columns = st.columns(columns_per_row)
        for column, field in zip(columns, visible_fields[start:start + columns_per_row]):
            column.metric(display_label(field), display_cell_value(field, row.get(field, "")))


def render_text_pair(label: str, value: object) -> None:
    st.caption(label)
    st.markdown(f"**{format_readable_text(value)}**")


def render_dashboard_style() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stMetric"] {
            padding: 0.1rem 0 0.35rem 0;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.82rem;
            line-height: 1.1;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.35rem;
            line-height: 1.18;
            white-space: normal;
            overflow-wrap: anywhere;
        }
        [data-testid="stMetricDelta"] {
            font-size: 0.8rem;
        }
        div[data-testid="stDataFrame"] {
            font-size: 0.88rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_how_to_use_card() -> None:
    st.info(
        "How to use this dashboard:\n\n"
        "1. Start with Top x10, Top x5, and Top x3 signals.\n"
        "2. Check Why It Ranked.\n"
        "3. Check Main Risk.\n"
        "4. If Review Required = Yes, inspect Review Flags.\n"
        "5. Use Candidate Card for deeper review.\n"
        "6. Do not treat any signal as a price forecast or investment recommendation."
    )


def render_explanation_center() -> None:
    with st.expander("Signal Glossary", expanded=False):
        st.caption("A compact guide for reading the numbers on this page.")
        for row_start in range(0, len(INFO_CARDS), 2):
            columns = st.columns(2)
            for column, (title, body) in zip(columns, INFO_CARDS[row_start:row_start + 2]):
                column.markdown(f"**{title}**")
                column.caption(body)


@st.cache_data(show_spinner=False)
def load_csv(name: str) -> pd.DataFrame:
    return load_demo_frame(name)


def load_dashboard_summary() -> dict[str, str]:
    return load_demo_summary()


def render_demo_sidebar() -> None:
    metadata = load_demo_metadata()
    st.sidebar.header("Demo View")
    st.sidebar.caption("View-only snapshot. The research pipeline and source files are not connected to this app.")
    generated_at = metadata.get("generated_at_utc")
    if generated_at:
        st.sidebar.caption(f"Data prepared: {generated_at}")


def render_status_banner(status_value: str) -> None:
    if status_value == "production_mvp_ready":
        st.success(format_display_value(status_value))
    elif status_value == "needs_fix":
        st.error(format_display_value(status_value))
    else:
        st.warning(format_display_value(status_value or "production_mvp_ready_with_data_gaps"))


def render_main_cockpit() -> None:
    summary = load_dashboard_summary()
    ranking = load_csv("final_research_ranking")

    st.subheader("Main Cockpit")
    st.markdown(
        "Crypto Research Lab ranks clean crypto candidates by emissions-adjusted x3/x5/x10 research signals.\n\n"
        "The dashboard is designed for research triage: identify what to review, why it surfaced, and what risks need manual validation."
    )
    st.caption(
        "This dashboard does not produce investment recommendations, buy/sell/hold decisions, portfolio weights, or price targets."
    )
    render_how_to_use_card()
    render_status_banner(summary.get("v1_0_status", ""))

    metric_keys = [
        "v1_0_status",
        "clean_candidate_count",
        "final_ranking_rows",
        "manual_qa_required_count",
        "missing_unlock_data_count",
        "calibration_status",
        "calculated_return_rows",
        "not_matured_return_rows",
    ]
    cols = st.columns(4)
    for idx, key in enumerate(metric_keys):
        cols[idx % 4].metric(display_label(key), format_display_value(summary.get(key, MISSING_VALUE_LABEL)))

    if ranking.empty:
        st.info("The demo ranking is unavailable.")
        return

    signal_modes = [
        ("Top x3 Research Signals", "x3_probability_emissions_adjusted_pct"),
        ("Top x5 Research Signals", "x5_probability_emissions_adjusted_pct"),
        ("Top x10 Research Signals", "x10_probability_emissions_adjusted_pct"),
    ]
    for title, probability_column in signal_modes:
        st.markdown(f"**{title}**")
        table = ranking.sort_values(
            by=[probability_column, "research_priority_score"],
            ascending=[False, False],
            na_position="last",
        ).head(5)
        visible_columns = _existing_columns(table, SIGNAL_COLUMNS)
        st.dataframe(display_dataframe(table[visible_columns]), width="stretch", hide_index=True)
        st.caption("Signals are heuristic research-prioritization metrics, not forecasts, price targets, or investment recommendations.")

    st.caption("These are research prioritization signals only, not investment recommendations.")
    render_explanation_center()


def render_asymmetry_table() -> None:
    ranking = load_csv("final_research_ranking")
    st.subheader("Asymmetry Table")
    if ranking.empty:
        st.info("The demo ranking is unavailable.")
        return

    focus_mode = st.selectbox("Focus", ["x3", "x5", "x10", "overall"])
    sort_column = {
        "x3": "x3_probability_emissions_adjusted_pct",
        "x5": "x5_probability_emissions_adjusted_pct",
        "x10": "x10_probability_emissions_adjusted_pct",
        "overall": "research_priority_score",
    }[focus_mode]

    filtered = ranking.copy()
    for column in ["sector", "research_priority_tier", "required_manual_review", "emissions_risk_bucket", "probability_confidence"]:
        if column not in filtered.columns:
            continue
        values = sorted(filtered[column].dropna().astype(str).unique().tolist())
        selected = st.multiselect(display_label(column), values, format_func=format_readable_text)
        if selected:
            filtered = filtered[filtered[column].astype(str).isin(selected)]

    if "market_cap_usd" in filtered.columns and not filtered["market_cap_usd"].dropna().empty:
        market_cap = pd.to_numeric(filtered["market_cap_usd"], errors="coerce")
        min_value, max_value = float(market_cap.min()), float(market_cap.max())
        selected_range = st.slider("Market Cap range", min_value, max_value, (min_value, max_value))
        filtered = filtered[market_cap.between(selected_range[0], selected_range[1], inclusive="both")]

    if "research_priority_score" in filtered.columns and not filtered["research_priority_score"].dropna().empty:
        score = pd.to_numeric(filtered["research_priority_score"], errors="coerce")
        min_score, max_score = float(score.min()), float(score.max())
        score_range = st.slider("Research Score range", min_score, max_score, (min_score, max_score))
        filtered = filtered[score.between(score_range[0], score_range[1], inclusive="both")]

    filtered = filtered.sort_values(by=sort_column, ascending=False, na_position="last")
    display = filtered[_existing_columns(filtered, ASYMMETRY_COLUMNS)]
    st.dataframe(display_dataframe(display), width="stretch", hide_index=True)
    render_explanation_center()


def render_candidate_card() -> None:
    factsheets = load_csv("candidate_factsheets")
    st.subheader("Candidate Card")
    if factsheets.empty:
        st.info("Candidate details are unavailable in this demo snapshot.")
        return

    options = (factsheets["symbol"].astype(str) + " - " + factsheets["name"].astype(str)).tolist()
    selected = st.selectbox("Candidate", options)
    row = factsheets.iloc[options.index(selected)]

    with st.container(border=True):
        st.markdown("**Identity**")
        identity_cols = st.columns(4)
        for column, field in zip(identity_cols, ["symbol", "name", "sector", "functional_category"]):
            if field in row.index:
                column.caption(display_label(field))
                column.markdown(f"**{display_cell_value(field, row.get(field, ''))}**")

    with st.container(border=True):
        st.markdown("**Research Signal**")
        render_metric_group(row, ["research_priority_score", "research_priority_tier", "required_manual_review"], columns_per_row=3)
        if "manual_review_reasons" in row.index:
            st.caption("Review Flags")
            st.markdown(f"**{display_cell_value('manual_review_reasons', row.get('manual_review_reasons', ''))}**")

    with st.container(border=True):
        st.markdown("**x3 / x5 / x10**")
        render_metric_group(
            row,
            [
                "base_x3_probability_pct",
                "base_x5_probability_pct",
                "base_x10_probability_pct",
                "adjusted_x3_probability_pct",
                "adjusted_x5_probability_pct",
                "adjusted_x10_probability_pct",
            ],
            columns_per_row=3,
        )

    with st.container(border=True):
        st.markdown("**Fundamentals**")
        render_metric_group(
            row,
            [
                "market_cap_usd",
                "fdv_usd",
                "tvl_usd",
                "revenue_30d_usd",
                "fees_30d_usd",
                "fundamental_score",
                "sector_relative_value_score",
            ],
            columns_per_row=4,
        )

    with st.container(border=True):
        st.markdown("**Risk / Confidence**")
        render_metric_group(
            row,
            [
                "emissions_risk_bucket",
                "emissions_adjustment_reason",
                "unlock_data_status",
                "historical_return_status",
                "calibration_status",
            ],
            columns_per_row=3,
        )

    with st.container(border=True):
        st.markdown("**Why It Ranked / Main Risk**")
        cols = st.columns(2)
        with cols[0]:
            render_text_pair("Why It Ranked", row.get("top_positive_signal", ""))
        with cols[1]:
            render_text_pair("Main Risk", row.get("top_risk_signal", ""))

    render_explanation_center()


def render_what_changed() -> None:
    changes = load_csv("run_change_report")
    st.subheader("What Changed")
    st.caption("Positive Rank Movement means the asset moved up. Negative means it moved down.")
    if changes.empty:
        st.info("Run-to-run changes are unavailable in this demo snapshot.")
        return

    filtered = changes.copy()
    if "status_change" in filtered.columns:
        values = sorted(filtered["status_change"].dropna().astype(str).unique().tolist())
        selected_status = st.multiselect("Change Status", values, format_func=format_readable_text)
        if selected_status:
            filtered = filtered[filtered["status_change"].astype(str).isin(selected_status)]

    rank_change = pd.to_numeric(filtered.get("rank_change", pd.Series(dtype=float)), errors="coerce")
    direction = st.selectbox("Rank movement", ["all", "positive rank change", "negative rank change", "no change"])
    if direction == "positive rank change":
        filtered = filtered[rank_change > 0]
    elif direction == "negative rank change":
        filtered = filtered[rank_change < 0]
    elif direction == "no change":
        filtered = filtered[rank_change.fillna(0) == 0]

    visible_columns = _existing_columns(filtered, CHANGE_COLUMNS)
    st.dataframe(display_dataframe(filtered[visible_columns]), width="stretch", hide_index=True)
    render_explanation_center()


def main() -> None:
    st.set_page_config(page_title="Crypto Research Lab", layout="wide")
    render_dashboard_style()
    st.title("Crypto Research Lab Decision Dashboard")
    render_demo_sidebar()

    tabs = st.tabs(["Main Cockpit", "Asymmetry Table", "Candidate Card", "What Changed"])
    with tabs[0]:
        render_main_cockpit()
    with tabs[1]:
        render_asymmetry_table()
    with tabs[2]:
        render_candidate_card()
    with tabs[3]:
        render_what_changed()


if __name__ == "__main__":
    main()
