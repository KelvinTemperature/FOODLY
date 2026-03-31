# FOODLY Kuwait

FOODLY is a modern full-stack food delivery app for Kuwait with:
- Responsive web and mobile-first UI
- Account registration and login (JWT)
- Cart, checkout, and order tracking references
- 50-slide Kuwait market sample meal carousel in frontend
- Payment methods: KNET, Visa, Mastercard, Apple Pay, cash on delivery
- Payment gateway support with Stripe integration when STRIPE_SECRET_KEY is provided
- Kuwait governorate delivery fees and backend pricing validation
- Role-based admin management APIs (users, shops, products, orders)

## Authors

- Givforks <givens.abraham@gmail.com>
- Kelvin Chukwuka <koolkt10@gmail.com>
- Givens Emmah Abraham <givens.abraham@live.com>

## Stack

- Backend: Flask, Flask-Smorest, Flask-SQLAlchemy, Flask-JWT-Extended
- Database: SQLite by default (DATABASE_URL configurable)
- Frontend: HTML, CSS, Vanilla JavaScript
- Optional payment provider: Stripe (fallback mock gateway enabled)

## Local Run

### Backend

1. Go to backend folder:
   - cd backend/Foodly
2. Install dependencies:
   - pip install -r requirements.txt
3. Create environment file:
   - cp .env.example .env
4. Start API:
   - python app.py

Backend default URL: http://127.0.0.1:5000

### Frontend

Open the main page in browser:
- frontend/index.html

`index1.html` redirects to `index.html` to avoid duplicate UI.

For live checkout, backend must be running.

## Deploy With Docker

From project root:
- docker compose up --build

Services:
- Frontend: http://127.0.0.1:8080
- Backend: http://127.0.0.1:5000

You can set these env vars before compose up:
- JWT_SECRET_KEY
- STRIPE_SECRET_KEY
- FOODLY_ADMIN_EMAIL
- FOODLY_ADMIN_PASSWORD
- FOODLY_ADMIN_NAME
- FOODLY_ADMIN_PHONE

## Admin Account

On startup, FOODLY creates (or promotes) a default admin account:
- email: givens.abraham@gmail.com
- password: Admin@12345

Use this account to call admin-protected endpoints and manage the platform.

Admin endpoints:
- GET /admin/users
- PUT /admin/users/<id>/role

## API Endpoints

### Health and Catalog
- GET /health
- GET /catalog

### Auth
- POST /auth/register
- POST /auth/login

### Shops
- GET /shops
- POST /shops (admin)
- GET /shops/<id>
- PUT /shops/<id> (admin)
- DELETE /shops/<id> (admin)

### Products
- GET /products
- POST /products (admin)
- GET /products/<id>
- PUT /products/<id> (admin)
- DELETE /products/<id> (admin)

### Orders
- GET /orders
- POST /orders
- GET /orders/<id>
- PUT /orders/<id> (admin)
- DELETE /orders/<id> (admin)

## Frontend Notes

- Slogan: "Foodly is better"
- Rival market slider values are sample benchmark estimates for comparison only.
- 50 meal samples use web-hosted PNG food icons (Twemoji CDN) mapped by meal type.
- Menu and slider images use lazy loading and async decoding for faster page load.

## Payment Behavior

- cash_on_delivery: payment_status = pending
- knet / visa / mastercard / apple_pay:
  - Uses Stripe PaymentIntent when STRIPE_SECRET_KEY is configured
  - Falls back to mock gateway when key is not provided
  - payment_status = authorized

## Test

From backend folder:
- python -m pytest -q
