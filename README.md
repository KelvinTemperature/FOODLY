FOODLY

![Foodly Logo](frontend/Images/Logo.png)

Foodly is a simple food-ordering web app with:
- A static frontend in `frontend/`
- A Flask REST backend in `backend/Foodly/`

## Backend Setup

1. Open a terminal in `backend/Foodly/`.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
python app.py
```

The API starts on `http://127.0.0.1:5000` by default.
Swagger UI is available at:

`http://127.0.0.1:5000/swagger-ui`

## Frontend Usage

Open `frontend/index.html` (home page) or `frontend/index1.html` (menu/order page) in a browser.

## Run Tests

From `backend/Foodly/`:

```bash
pip install -r requirements.txt
pytest -q
```

## Available API Endpoints

Products:
- `GET /products`
- `POST /products`
- `GET /products/<product_id>`
- `PUT /products/<product_id>`
- `DELETE /products/<product_id>`

Shops:
- `GET /shops`
- `POST /shops`
- `GET /shops/<shop_id>`
- `PUT /shops/<shop_id>`
- `DELETE /shops/<shop_id>`

Orders:
- `GET /orders`
- `POST /orders`
- `GET /orders/<order_id>`
- `PUT /orders/<order_id>`
- `DELETE /orders/<order_id>`

