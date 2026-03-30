import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")

    from app import create_app

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def create_shop(client):
    response = client.post(
        "/shops",
        json={
            "name": "Main Branch",
            "address": "12 Food Street",
            "phone": "08000000000",
            "email": "shop@example.com",
        },
    )
    assert response.status_code == 201
    return response.get_json()["id"]


def create_product(client, shop_id):
    response = client.post(
        "/products",
        json={
            "name": "Refuel Fried Rice Meal",
            "description": "Combo meal",
            "price": 1500,
            "quantity": 8,
            "shop_id": shop_id,
        },
    )
    assert response.status_code == 201
    return response.get_json()["id"]


def test_shop_product_order_crud_flow(client):
    shop_id = create_shop(client)
    product_id = create_product(client, shop_id)

    order_create = client.post(
        "/orders",
        json={
            "product_id": product_id,
            "quantity": 2,
        },
    )
    assert order_create.status_code == 201
    order_body = order_create.get_json()
    order_id = order_body["id"]
    assert order_body["quantity"] == 2
    assert order_body["product_id"] == product_id

    order_get = client.get(f"/orders/{order_id}")
    assert order_get.status_code == 200

    order_update = client.put(
        f"/orders/{order_id}",
        json={"quantity": 3},
    )
    assert order_update.status_code == 200
    assert order_update.get_json()["quantity"] == 3

    order_list = client.get("/orders")
    assert order_list.status_code == 200
    assert len(order_list.get_json()) == 1

    order_delete = client.delete(f"/orders/{order_id}")
    assert order_delete.status_code == 204

    order_not_found = client.get(f"/orders/{order_id}")
    assert order_not_found.status_code == 404


def test_products_and_shops_list(client):
    shop_id = create_shop(client)
    create_product(client, shop_id)

    shops_response = client.get("/shops")
    assert shops_response.status_code == 200
    assert len(shops_response.get_json()) == 1

    products_response = client.get("/products")
    assert products_response.status_code == 200
    assert len(products_response.get_json()) == 1


def test_missing_order_returns_404(client):
    response = client.get("/orders/999999")
    assert response.status_code == 404
