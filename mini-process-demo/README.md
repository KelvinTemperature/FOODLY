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

```bash
cd mini-process-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open the frontend by serving the `frontend` folder, for example:

```bash
cd frontend
python -m http.server 5501
```

Then open:

```text
http://127.0.0.1:5501
```

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
