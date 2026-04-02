import pytest

@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    monkeypatch.setenv("MONGO_URI", "mongomock://localhost")
    monkeypatch.setenv("MONGO_DB_NAME", "foodly_test_orders")
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def get_admin_token(client):
    response = client.post(
        "/auth/login",
        json={"email": "givens.abraham@gmail.com", "password": "Admin@12345"},
    )
    assert response.status_code == 200
    return response.get_json()["access_token"]

def create_shop(client, token):
    response = client.post(
        "/shops",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Kuwait City Kitchen",
            "address": "12 Gulf Road, Kuwait City",
            "phone": "+96522001234",
            "email": "shop@foodlykw.com",
        },
    )
    assert response.status_code == 201
    return response.get_json()["id"]

def create_product(client, shop_id, token):
    response = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Machboos Chicken Bowl",
            "description": "Traditional Kuwaiti rice bowl",
            "price": 2.75,
            "quantity": 8,
            "shop_id": shop_id,
        },
    )
    assert response.status_code == 201
    return response.get_json()["id"]

def test_shop_product_order_crud_flow(client):
    admin_token = get_admin_token(client)
    shop_id = create_shop(client, admin_token)
    product_id = create_product(client, shop_id, admin_token)
    order_create = client.post(
        "/orders",
        json={
            "product_id": product_id,
            "quantity": 2,
            "customer_name": "Givforks",
            "customer_phone": "+96567778899",
            "customer_email": "givens.abraham@gmail.com",
            "delivery_address": "Salmiya Block 10, Street 4",
            "governorate": "Hawalli",
            "payment_method": "knet",
            "notes": "No onions please",
        },
    )
    assert order_create.status_code == 201
    order_body = order_create.get_json()
    order_id = order_body["id"]
    assert order_body["quantity"] == 2
    assert order_body["product_id"] == product_id
    assert order_body["payment_status"] == "authorized"
    assert order_body["payment_reference"]
    assert order_body["order_status"] == "confirmed"
    assert order_body["subtotal"] == pytest.approx(5.5)
    assert order_body["delivery_fee"] == pytest.approx(1.25)
    assert order_body["total_amount"] == pytest.approx(6.75)
    order_get = client.get(f"/orders/{order_id}")
    assert order_get.status_code == 200
    order_update = client.put(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"quantity": 3},
    )
    assert order_update.status_code == 200
    assert order_update.get_json()["quantity"] == 3
    order_list = client.get("/orders")
    assert order_list.status_code == 200
    assert len(order_list.get_json()) == 1
    order_delete = client.delete(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert order_delete.status_code == 204
    order_not_found = client.get(f"/orders/{order_id}")
    assert order_not_found.status_code == 404

def test_products_and_shops_list(client):
    admin_token = get_admin_token(client)
    shop_id = create_shop(client, admin_token)
    create_product(client, shop_id, admin_token)
    shops_response = client.get("/shops")
    assert shops_response.status_code == 200
    assert len(shops_response.get_json()) == 1
    products_response = client.get("/products")
    assert products_response.status_code == 200
    assert len(products_response.get_json()) == 1

def test_missing_order_returns_404(client):
    response = client.get("/orders/999999")
    assert response.status_code == 404


def test_insufficient_stock_returns_400(client):
    admin_token = get_admin_token(client)
    shop_id = create_shop(client, admin_token)
    product_id = create_product(client, shop_id, admin_token)
    response = client.post(
        "/orders",
        json={"product_id": product_id, "quantity": 200, "governorate": "Al Asimah"},
    )
    assert response.status_code == 400


def test_catalog_endpoint(client):
    admin_token = get_admin_token(client)
    shop_id = create_shop(client, admin_token)
    create_product(client, shop_id, admin_token)
    response = client.get("/catalog")
    assert response.status_code == 200
    body = response.get_json()
    assert body["country"] == "Kuwait"
    assert body["currency"] == "KWD"
    assert len(body["shops"]) == 1
    assert len(body["products"]) == 1


def test_auth_register_login_and_checkout(client):
    admin_token = get_admin_token(client)
    shop_id = create_shop(client, admin_token)
    product_id = create_product(client, shop_id, admin_token)

    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Givforks",
            "email": "givens.customer@gmail.com",
            "phone": "+96567778899",
            "password": "securepass123",
        },
    )
    assert register_response.status_code == 201
    register_body = register_response.get_json()
    token = register_body["access_token"]
    assert token

    login_response = client.post(
        "/auth/login",
        json={"email": "givens.customer@gmail.com", "password": "securepass123"},
    )
    assert login_response.status_code == 200

    order_response = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "product_id": product_id,
            "quantity": 1,
            "customer_name": "Givforks",
            "customer_phone": "+96567778899",
            "delivery_address": "Kuwait City",
            "governorate": "Al Asimah",
            "payment_method": "visa",
        },
    )
    assert order_response.status_code == 201
    order_body = order_response.get_json()
    assert order_body["user_id"] == register_body["user"]["id"]
    assert order_body["payment_status"] == "authorized"


def test_non_admin_cannot_create_shop(client):
    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Normal User",
            "email": "normal.user@example.com",
            "password": "securepass123",
        },
    )
    token = register_response.get_json()["access_token"]

    response = client.post(
        "/shops",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Restricted Shop",
            "address": "Kuwait City",
            "phone": "+96522001234",
            "email": "restricted@foodlykw.com",
        },
    )
    assert response.status_code == 403


def test_admin_can_list_users(client):
    admin_token = get_admin_token(client)
    response = client.get("/admin/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["users"]
