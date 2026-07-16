# Crypto Research Lab Demo

Read-only Streamlit demo for the Crypto Research Lab dashboard.

The application contains only a prepared, column-limited demo bundle. It does not contain or connect to the research pipeline, source CSV/Excel files, historical snapshots, manual overrides, update scripts, logs, or local filesystem paths.

The four dashboard tabs, all rows and columns visible in the local dashboard, filters, candidate cards, and the complete Signal Glossary remain available in the demo.

## Local preview

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app/streamlit_app.py
```

Open `http://localhost:8501`.

## Data boundary

- The repository must remain private.
- The hosted app may be public.
- `demo_data/demo_bundle.sqlite3` contains only values intentionally exposed in the UI.
- There is no data download button and no pipeline update action.
- A visitor can still copy values visible in the browser. Hidden source data is not included in the bundle.

See [docs/DEPLOY.md](docs/DEPLOY.md) for the deployment checklist.
