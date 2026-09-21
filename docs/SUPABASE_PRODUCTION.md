# Supabase production (`smart-hub-prod`)

This tree uses **only** the production Postgres project.

| Field | Value |
|-------|--------|
| **Project name** | `smart-hub-prod` |
| **Project URL** | `https://nfyccectlkvvmemveoxn.supabase.co` |
| **Project ref** | `nfyccectlkvvmemveoxn` |
| **Region** | Canada (`ca-central-1`) |

## Connection string

1. Dashboard **Connect** → **Direct** → **Session pooler** → **URI**
2. Replace `[YOUR-PASSWORD]` locally (do not type it into the Connect dialog)
3. Append `?sslmode=require` if missing

Example shape:

`postgresql://postgres.nfyccectlkvvmemveoxn:[YOUR-PASSWORD]@aws-0-ca-central-1.pooler.supabase.com:5432/postgres?sslmode=require`

Put that URI in `.streamlit/secrets.toml` with `APP_ENV = "production"`.

## Migrations

From this folder:

```powershell
$env:APP_ENV = "production"
python admin_tools/run_migrations.py --require-prod
```

Then **Table Editor** should show `legal_consents`, `screener_snapshots`, and `schema_migrations`.

## Snapshots

```powershell
$env:APP_ENV = "production"
python admin_tools/screener_worker.py
```

GitHub Actions: `.github/workflows/screener-snapshots.yml` (`APP_ENV=production`). Set repo secrets `DATABASE_URL` (this project only) and `ALPHA_VANTAGE_API_KEY`.
