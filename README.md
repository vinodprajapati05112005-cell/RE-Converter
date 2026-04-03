# Regex Automata Explorer

Theory of Computation — Formal Regular Expressions over {0,1} and {b,c}.

## Run Locally

```bash
cd regex-automata/backend
pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000

## Deploy on Railway

1. Push this repo to GitHub
2. Go to https://railway.app → New Project → Deploy from GitHub
3. Set root directory to `regex-automata/backend`
4. Add environment variables (see below)

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Any long random string |
| `DEBUG` | No | Set to `False` in production (default) |
| `ALLOWED_HOSTS` | No | Comma-separated hostnames e.g. `myapp.railway.app` |
| `PORT` | Auto | Set automatically by Railway/Render |

## API Endpoints

- `GET  /api/patterns/` — list all patterns
- `GET  /api/patterns/<key>/` — pattern detail
- `POST /api/validate/` — validate a binary string
- `POST /api/nlp/` — natural language to RE
