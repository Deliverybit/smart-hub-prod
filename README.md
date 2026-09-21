# Smart Hub Prod

Production tree for **The Scoop 52** — Streamlit market screener with legal consent logging to Supabase (`smart-hub-prod`).

| Environment | Supabase project | `APP_ENV` |
|-------------|------------------|-----------|
| Production | `smart-hub-prod` | `production` |

## Run locally

**Windows:**

```powershell
.\launch.ps1
```

The launcher uses `APP_ENV=production`. Edit `.streamlit/secrets.toml` with the **smart-hub-prod** Session pooler URI (never the staging database).

**Manual:**

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
python -m streamlit run app.py
```

## Database

See [docs/SUPABASE_PRODUCTION.md](docs/SUPABASE_PRODUCTION.md).

```bash
python admin_tools/run_migrations.py --require-prod
python admin_tools/screener_worker.py
```

## Secrets (never commit)

- `.streamlit/secrets.toml` — local / host secrets
- `DATABASE_URL` — **smart-hub-prod** Session pooler URI with `?sslmode=require`
