# Hosted demo deployment

## Required security boundary

1. Create a new **private** GitHub repository for this demo only.
2. Do not copy the main research repository into it.
3. Confirm the repository contains no source CSV/Excel files, pipeline modules, historical snapshots, manual overrides, logs, secrets, or local paths.
4. Connect the private repository to the Streamlit hosting account.
5. Set the application entry point to `app/streamlit_app.py`.
6. Keep the app view-only. No secrets are required for the prepared demo bundle.

## Updating demo data

Generate a new demo bundle locally from the private research project, run the security tests, review the visible tables, then replace only `demo_data/demo_bundle.sqlite3` in this repository.

Do not run the research pipeline from the hosted app and do not add API credentials to the demo repository.

## Pre-publish checks

```bash
.venv/bin/python -m pytest
.venv/bin/python -m streamlit run app/streamlit_app.py
```

Verify all four tabs, filters, candidate cards, and run-change values before publishing.

