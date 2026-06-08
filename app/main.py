import mimetypes
from app.config import Config
from app.db import Db
from flask import Flask, render_template, redirect, send_from_directory
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

mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('text/css', '.css')
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

@app.route("/client/")
def client():
	return render_template("client/index.html")

@app.route("/")
def default():
	return redirect('/client')

@app.route("/client/index/")
def client_index():
	return redirect('/client')

@app.route("/login/")
def login():
	return render_template("login.html")

@app.route("/client/register/")
def client_register():
	return render_template("client/register.html")

@app.route("/client/profile/")
def client_profile():
	return render_template("client/profile.html")

@app.route("/client/cart/")
def client_cart():
	return render_template("client/cart.html")

@app.route("/client/wishlist/")
def client_wishlist():
	return render_template("client/wishlist.html")

@app.route("/client/orders/")
def client_orders():
	return render_template("client/orders.html")

@app.route("/client/order_payments/")
def client_order_payments():
	return render_template("client/order_payments.html")

@app.route("/client/product_reviews/")
def client_product_reviews():
	return render_template("client/product_reviews.html")

@app.route('/client/make-order/')
def client_make_order():
	return render_template("client/make_order.html")

@app.route('/client/order/<int:order_id>')
def client_order(order_id: int):
	return render_template("client/order.html", order_id=order_id)

@app.route('/client/product/<int:product_id>')
def client_product(product_id: int):
	return render_template("client/product.html", product_id=product_id)

@app.route("/employee/")
def employee():
	return render_template("employee/index.html")

@app.route("/employee/products/")
def employee_products():
	return render_template("employee/products.html")

@app.route("/employee/create-product/")
def employee_create_product():
	return render_template("employee/create_product.html")

@app.route("/employee/users/")
def employee_users():
	return render_template("employee/users.html")

@app.route("/employee/user/<int:user_id>")
def employee_user(user_id: int):
	return render_template("employee/user.html", user_id=user_id)

@app.route("/employee/permissions/")
def employee_permissions():
	return render_template("employee/permissions.html")

@app.route("/employee/create-permission/")
def employee_create_permission():
	return render_template("employee/create_permission.html")

@app.route("/employee/permission/<int:permission_id>")
def employee_permission(permission_id: int):
	return render_template("employee/permission.html", permission_id=permission_id)

@app.route("/employee/roles/")
def employee_roles():
	return render_template("employee/roles.html")

@app.route("/employee/create-role/")
def employee_create_role():
	return render_template("employee/create_role.html")

@app.route("/employee/role/<int:role_id>")
def employee_role(role_id: int):
	return render_template("employee/role.html", role_id=role_id)

@app.route("/employee/employees/")
def employee_employees():
	return render_template("employee/employees.html")

@app.route("/employee/employee/<int:employee_id>")
def employee_employee(employee_id: int):
	return render_template("employee/employee.html", employee_id=employee_id)

@app.route("/employee/create-employee/")
def employee_create_employee():
	return render_template("employee/create_employee.html")

@app.route("/employee/suppliers/")
def employee_suppliers():
	return render_template("employee/suppliers.html")

@app.route("/employee/create-supplier/")
def employee_create_supplier():
	return render_template("employee/create_supplier.html")

@app.route("/employee/supplier/<int:supplier_id>")
def employee_supplier(supplier_id: int):
	return render_template("employee/supplier.html", supplier_id=supplier_id)

@app.route("/employee/warehouses/")
def employee_warehouses():
	return render_template("employee/warehouses.html")

@app.route("/employee/create-warehouse/")
def employee_create_warehouse():
	return render_template("employee/create_warehouse.html")

@app.route("/employee/warehouse/<int:warehouse_id>")
def employee_warehouse(warehouse_id: int):
	return render_template("employee/warehouse.html", warehouse_id=warehouse_id)

@app.route("/employee/warehouse/<int:warehouse_id>/supplies")
def employee_supplies(warehouse_id: int):
	return render_template("employee/supplies.html", warehouse_id=warehouse_id)

@app.route("/employee/warehouse/<int:warehouse_id>/create-supply")
def employee_create_supply(warehouse_id: int):
	return render_template("employee/create_supply.html", warehouse_id=warehouse_id)

@app.route("/employee/supply/<int:supply_id>")
def employee_supply(supply_id: int):
	return render_template("employee/supply.html", supply_id=supply_id)

@app.route('/image/<path:filename>/')
def get_image(filename):
	return send_from_directory(Config.PATH_IMAGES, filename)
