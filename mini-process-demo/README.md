# Mini Process Demo

A small end-to-end project to understand the full workflow:

- backend API
- simple frontend
- tests
- environment setup

## What it does

A tiny task tracker with:

- `GET /health`
- `GET /tasks`
- `POST /tasks`
- `DELETE /tasks/<id>`

## Files

- `app.py` - Flask API
- `frontend/index.html` - UI
- `frontend/app.js` - UI logic
- `frontend/style.css` - basic styling
- `tests/test_app.py` - API tests
- `.env.example` - example environment file

## Run

Fastest way:

```bash
cd mini-process-demo
bash start.sh
```

Manual way:

```bash
cd mini-process-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5001
```

Optional: if you want to serve frontend separately, run a static server in `frontend/` and it will still talk to backend on port 5001.

## Troubleshooting

- Do not run `python3 frontend/app.js`. That file is JavaScript and runs in the browser.
- Do not run `python3 frontend/index.html`. HTML must be opened by the browser.
- Correct command is `python app.py` from this folder, or just `bash start.sh`.

## Test

```bash
pytest -q
```

## Learning flow

1. Start with the API.
2. Add a frontend that calls the API.
3. Add tests.
4. Verify everything locally.
5. Extend one piece at a time.
