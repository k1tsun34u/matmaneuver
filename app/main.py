from app.db import Db
from flask import Flask, render_template
from app.routers.api.client.auth import client_auth_bp
from app.routers.api.client.products import client_products_bp
from app.routers.api.client.product_categories import client_product_categories_bp
from app.routers.api.client.product_images import client_product_images_bp
from app.routers.api.client.product_reviews import client_product_reviews_bp
from app.routers.api.client.orders import client_orders_bp
from app.routers.api.client.carts import client_carts_bp
from app.routers.api.client.order_payments import client_order_payments_bp
from app.routers.api.employee.employees import employee_employees_bp
from app.routers.api.employee.users import employee_users_bp


Db.init("localhost", 5432, "matmaneuver", "postgres")

app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(client_auth_bp)
app.register_blueprint(client_products_bp)
app.register_blueprint(client_product_categories_bp)
app.register_blueprint(client_product_images_bp)
app.register_blueprint(client_product_reviews_bp)
app.register_blueprint(client_orders_bp)
app.register_blueprint(client_order_payments_bp)
app.register_blueprint(client_carts_bp)
app.register_blueprint(employee_employees_bp)
app.register_blueprint(employee_users_bp)

@app.route("/")
def main():
	return render_template("client/index.html")
