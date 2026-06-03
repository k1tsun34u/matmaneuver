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
from app.routers.api.employee.categories import employee_categories_bp
from app.routers.api.employee.permissions import employee_permissions_bp
from app.routers.api.employee.roles import employee_roles_bp
from app.routers.api.employee.warehouses import employee_warehouses_bp
from app.routers.api.employee.write_offs import employee_write_offs_bp
from app.routers.api.employee.orders import employee_orders_bp
from app.routers.api.employee.order_fulfillments import employee_order_fulfillments_bp
from app.routers.api.employee.order_payments import employee_order_payments_bp
from app.routers.api.employee.product_categories import employee_product_categories_bp
from app.routers.api.employee.product_images import employee_product_images_bp
from app.routers.api.employee.product_reviews import employee_product_reviews_bp
from app.routers.api.employee.products import employee_products_bp
from app.routers.api.employee.suppliers import employee_suppliers_bp
from app.routers.api.employee.supplies import employee_supplies_bp


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
app.register_blueprint(employee_categories_bp)
app.register_blueprint(employee_permissions_bp)
app.register_blueprint(employee_roles_bp)
app.register_blueprint(employee_warehouses_bp)
app.register_blueprint(employee_write_offs_bp)
app.register_blueprint(employee_orders_bp)
app.register_blueprint(employee_order_fulfillments_bp)
app.register_blueprint(employee_order_payments_bp)
app.register_blueprint(employee_product_categories_bp)
app.register_blueprint(employee_product_images_bp)
app.register_blueprint(employee_product_reviews_bp)
app.register_blueprint(employee_products_bp)
app.register_blueprint(employee_suppliers_bp)
app.register_blueprint(employee_supplies_bp)

@app.route("/")
def main():
	return render_template("client/index.html")
