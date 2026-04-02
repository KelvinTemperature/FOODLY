# Foodly Backend

Flask + Flask-Smorest API for Foodly.

## Database Setup

- MySQL stores auth and catalog data (`users`, `shops`, `products`).
- MongoDB stores order documents.

Set environment variables before running:

```bash
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_USER=your_mysql_user
export MYSQL_PASSWORD=your_mysql_password
export MYSQL_DATABASE=foodly_auth
export MONGO_URI='mongodb+srv://...'
export MONGO_DB_NAME=foodly_orders
export DB_WAIT_TIMEOUT_SECONDS=90
export DB_WAIT_INTERVAL_SECONDS=3
```

Optional:

- `DATABASE_URL` overrides all MySQL variables when provided.
- `JWT_SECRET_KEY` sets the JWT signing key.
- `DB_WAIT_TIMEOUT_SECONDS` and `DB_WAIT_INTERVAL_SECONDS` control startup wait behavior.

## Run

```bash
pip install -r requirements.txt
python app.py
```

## Docs

Swagger UI: `http://127.0.0.1:5000/swagger-ui`

Health endpoints:

- `GET /health` (service + MySQL/Mongo status)
- `GET /health/db` (database-only status)

Container startup runs `/app/start.sh`, which blocks until MySQL and MongoDB are reachable before launching Gunicorn.
