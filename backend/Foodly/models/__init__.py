from models.shop import ShopModel
from models.product import ProductModel
from models.order import OrderModel

cd ~/projects/FOODLY/backend/Foodly
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v