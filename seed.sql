BEGIN;

-- ==========================
-- users / employees
-- ==========================

INSERT INTO users (phone, email, full_name, password_hash, blocked_by, blocked_at, deleted_by, deleted_at, created_by)
VALUES
	('+79990000001', 'owner@matmaneuver.local', 'Owner User', 'hash_owner', NULL, NULL, NULL, NULL, NULL),
	('+79990000002', 'manager@matmaneuver.local', 'Warehouse Manager', 'hash_manager', NULL, NULL, NULL, NULL, NULL),
	('+79990000003', 'support@matmaneuver.local', 'Support Agent', 'hash_support', NULL, NULL, NULL, NULL, NULL),
	('+79990000004', 'alice@client.local', 'Alice Client', 'hash_alice', NULL, NULL, NULL, NULL, NULL),
	('+79990000005', 'bob@client.local', 'Bob Client', 'hash_bob', NULL, NULL, NULL, NULL, NULL),
	('+79990000006', 'charlie@client.local', 'Charlie Client', 'hash_charlie', NULL, NULL, NULL, NULL, NULL);

INSERT INTO employees (user_id, hired_by, hired_at, fired_by, fired_at, created_by)
VALUES
	((SELECT id FROM users WHERE phone = '+79990000001'), NULL, NOW() - INTERVAL '39 days', NULL, NULL, NULL),
	((SELECT id FROM users WHERE phone = '+79990000002'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')), NOW() - INTERVAL '34 days', NULL, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM users WHERE phone = '+79990000003'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')), NOW() - INTERVAL '29 days', NULL, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

UPDATE users
SET created_by = (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))
WHERE phone IN ('+79990000002', '+79990000003', '+79990000004', '+79990000005', '+79990000006');

UPDATE users
SET blocked_by = (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003')),
	blocked_at = NOW() - INTERVAL '2 days'
WHERE phone = '+79990000006';

-- ==========================
-- roles / permissions / mappings
-- ==========================

INSERT INTO roles (code, is_system, deactivated_by, created_by)
VALUES
	('super_admin', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('warehouse', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('support', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

INSERT INTO permissions (code, description, is_system, deactivated_by, created_by)
VALUES
	('create_user', 'Permission: create_user', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('block_user', 'Permission: block_user', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('unblock_user', 'Permission: unblock_user', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('delete_user', 'Permission: delete_user', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_employee', 'Permission: create_employee', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('hire', 'Permission: hire', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('fire', 'Permission: fire', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_permission', 'Permission: create_permission', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('assign_permission', 'Permission: assign_permission', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('unassign_permission', 'Permission: unassign_permission', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('deactivate_permission', 'Permission: deactivate_permission', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('set_permission_description', 'Permission: set_permission_description', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_role', 'Permission: create_role', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('deactivate_role', 'Permission: deactivate_role', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('assign_role', 'Permission: assign_role', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('unassign_role', 'Permission: unassign_role', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_warehouse', 'Permission: create_warehouse', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('delete_warehouse', 'Permission: delete_warehouse', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('set_warehouse_description', 'Permission: set_warehouse_description', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('add_warehouse_product', 'Permission: add_warehouse_product', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('delete_warehouse_product', 'Permission: delete_warehouse_product', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_product', 'Permission: create_product', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('delete_product', 'Permission: delete_product', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('set_product_price', 'Permission: set_product_price', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('set_product_description', 'Permission: set_product_description', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('assign_product_category', 'Permission: assign_product_category', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('unassign_product_category', 'Permission: unassign_product_category', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_product_image', 'Permission: create_product_image', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('delete_product_image', 'Permission: delete_product_image', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_supplier', 'Permission: create_supplier', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('deactivate_supplier', 'Permission: deactivate_supplier', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('set_supplier_fields', 'Permission: set_supplier_fields', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_supply', 'Permission: create_supply', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('set_supply_status', 'Permission: set_supply_status', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_supply_item', 'Permission: create_supply_item', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('delete_supply_item', 'Permission: delete_supply_item', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('set_order_status', 'Permission: set_order_status', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_write_off', 'Permission: create_write_off', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('delete_write_off', 'Permission: delete_write_off', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('create_write_off_item', 'Permission: create_write_off_item', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('delete_write_off_item', 'Permission: delete_write_off_item', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('delete_product_review', 'Permission: delete_product_review', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

INSERT INTO role_permissions (role_id, permission_id, assigned_by)
SELECT
	(SELECT id FROM roles WHERE code = 'super_admin'),
	p.id,
	(SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))
FROM permissions p;

INSERT INTO role_permissions (role_id, permission_id, assigned_by)
VALUES
	((SELECT id FROM roles WHERE code = 'warehouse'), (SELECT id FROM permissions WHERE code = 'add_warehouse_product'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM roles WHERE code = 'warehouse'), (SELECT id FROM permissions WHERE code = 'create_supply'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM roles WHERE code = 'support'), (SELECT id FROM permissions WHERE code = 'delete_product_review'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

INSERT INTO employee_roles (employee_id, role_id, assigned_by)
VALUES
	((SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')), (SELECT id FROM roles WHERE code = 'super_admin'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002')), (SELECT id FROM roles WHERE code = 'warehouse'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003')), (SELECT id FROM roles WHERE code = 'support'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

-- ==========================
-- warehouses / categories / products
-- ==========================

INSERT INTO warehouses (address, description, deleted_by, created_by)
VALUES
	('123 North St, City A', 'Main warehouse', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('456 East St, City B', 'Reserve warehouse', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

INSERT INTO categories (parent_category_id, name, deactivated_by, created_by)
VALUES
	(NULL, 'Electronics', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM categories WHERE name = 'Electronics'), 'Laptops', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM categories WHERE name = 'Electronics'), 'Accessories', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

INSERT INTO products (name, description, price, deleted_by, created_by)
VALUES
	('Laptop Pro 14', '14-inch productivity laptop', 1599.99, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('Wireless Mouse X', 'Ergonomic wireless mouse', 49.90, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('USB-C Dock 9in1', 'Docking station for laptops', 119.00, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

INSERT INTO product_categories (product_id, category_id, assigned_by)
VALUES
	((SELECT id FROM products WHERE name = 'Laptop Pro 14'), (SELECT id FROM categories WHERE name = 'Laptops'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM products WHERE name = 'Wireless Mouse X'), (SELECT id FROM categories WHERE name = 'Accessories'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), (SELECT id FROM categories WHERE name = 'Accessories'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

INSERT INTO product_images (product_id, storage_key, created_by)
VALUES
	((SELECT id FROM products WHERE name = 'Laptop Pro 14'), 'products/1/main.jpg', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM products WHERE name = 'Wireless Mouse X'), 'products/2/main.jpg', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 'products/3/main.jpg', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

INSERT INTO warehouse_products (product_id, warehouse_id, created_by)
VALUES
	((SELECT id FROM products WHERE name = 'Laptop Pro 14'), (SELECT id FROM warehouses WHERE address = '123 North St, City A'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT id FROM products WHERE name = 'Wireless Mouse X'), (SELECT id FROM warehouses WHERE address = '123 North St, City A'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), (SELECT id FROM warehouses WHERE address = '123 North St, City A'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT id FROM products WHERE name = 'Laptop Pro 14'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT id FROM products WHERE name = 'Wireless Mouse X'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002')));

-- ==========================
-- suppliers / supplies
-- ==========================

INSERT INTO suppliers (full_name, phone, email, address, deactivated_by, created_by)
VALUES
	('Tech Source LLC', '+78000000001', 'sales@techsource.local', 'Supplier Ave 10', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	('Parts Hub Inc', '+78000000002', 'hello@partshub.local', 'Industrial Rd 7', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001')));

INSERT INTO supplies (supplier_id, warehouse_id, planned_delivery_date, created_by)
VALUES
	((SELECT id FROM suppliers WHERE phone = '+78000000001'), (SELECT id FROM warehouses WHERE address = '123 North St, City A'), CURRENT_DATE - 8, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT id FROM suppliers WHERE phone = '+78000000002'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'), CURRENT_DATE + 2, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002')));

UPDATE supplies
SET current_status = 'delivered'
WHERE supplier_id = (SELECT id FROM suppliers WHERE phone = '+78000000001');

UPDATE supplies
SET current_status = 'in_transit'
WHERE supplier_id = (SELECT id FROM suppliers WHERE phone = '+78000000002');

INSERT INTO supply_items (supply_id, product_id, quantity, price)
VALUES
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 5, 1300.00),
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 50, 35.00),
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000002'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 20, 80.00);

INSERT INTO supply_status_history (supply_id, status, changed_by)
VALUES
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), 'confirmed', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), 'in_transit', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), 'delivered', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000002'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000002'), 'confirmed', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000001'))),
	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000002'), 'in_transit', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002')));

-- ==========================
-- orders / order history / fulfillment / payments
-- ==========================

INSERT INTO orders (track_number, delivery_address, created_by)
VALUES
	('TRK-2026-0001', 'Client Street 11, Apt 5', (SELECT id FROM users WHERE phone = '+79990000004')),
	('TRK-2026-0002', 'Client Avenue 99, Apt 12', (SELECT id FROM users WHERE phone = '+79990000005')),
	('TRK-2026-0003', 'Green Road 3, Apt 8', (SELECT id FROM users WHERE phone = '+79990000004'));

UPDATE orders SET current_status = 'confirmed' WHERE track_number = 'TRK-2026-0001';
UPDATE orders SET current_status = 'in_transit' WHERE track_number = 'TRK-2026-0002';

INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 1, 1599.99),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 2, 49.90),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1, 119.00),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 1, 49.90),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0003'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 1, 49.90);

INSERT INTO order_status_history (order_id, status, changed_by)
VALUES
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003'))),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), 'confirmed', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003'))),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003'))),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), 'confirmed', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003'))),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), 'in_transit', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0003'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003')));

INSERT INTO order_fulfillments (order_id, warehouse_id)
VALUES
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), (SELECT id FROM warehouses WHERE address = '123 North St, City A')),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'));

INSERT INTO order_fulfillment_items (order_fulfillment_id, product_id, quantity, price)
VALUES
	((SELECT ofl.id FROM order_fulfillments ofl JOIN orders o ON o.id = ofl.order_id WHERE o.track_number = 'TRK-2026-0001'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 1, 1599.99),
	((SELECT ofl.id FROM order_fulfillments ofl JOIN orders o ON o.id = ofl.order_id WHERE o.track_number = 'TRK-2026-0001'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 2, 49.90),
	((SELECT ofl.id FROM order_fulfillments ofl JOIN orders o ON o.id = ofl.order_id WHERE o.track_number = 'TRK-2026-0002'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1, 119.00),
	((SELECT ofl.id FROM order_fulfillments ofl JOIN orders o ON o.id = ofl.order_id WHERE o.track_number = 'TRK-2026-0002'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 1, 49.90);

INSERT INTO order_payments (order_id, amount, payment_method)
VALUES
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), 1699.79, 'card'),
	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), 168.90, 'sbp');

-- ==========================
-- write-offs
-- ==========================

INSERT INTO write_offs (warehouse_id, comment, created_by)
VALUES
	((SELECT id FROM warehouses WHERE address = '123 North St, City A'), 'Packaging damage during handling', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
	((SELECT id FROM warehouses WHERE address = '456 East St, City B'), 'Count mismatch found in cycle check', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002')));

UPDATE write_offs
SET reason = 'damaged'
WHERE warehouse_id = (SELECT id FROM warehouses WHERE address = '123 North St, City A');

UPDATE write_offs
SET reason = 'inventory_mismatch'
WHERE warehouse_id = (SELECT id FROM warehouses WHERE address = '456 East St, City B');

INSERT INTO write_off_items (write_off_id, product_id, quantity, price)
VALUES
	((SELECT wo.id FROM write_offs wo JOIN warehouses w ON w.id = wo.warehouse_id WHERE w.address = '123 North St, City A'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 3, 35.00),
	((SELECT wo.id FROM write_offs wo JOIN warehouses w ON w.id = wo.warehouse_id WHERE w.address = '456 East St, City B'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1, 80.00);

-- ==========================
-- carts / cart items
-- ==========================

INSERT INTO carts (user_id, type)
VALUES
	((SELECT id FROM users WHERE phone = '+79990000004'), 'active'),
	((SELECT id FROM users WHERE phone = '+79990000004'), 'wishlist'),
	((SELECT id FROM users WHERE phone = '+79990000005'), 'active'),
	((SELECT id FROM users WHERE phone = '+79990000005'), 'wishlist');

INSERT INTO cart_items (cart_id, product_id, quantity)
VALUES
	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000004' AND c.type = 'active'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1),
	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000004' AND c.type = 'wishlist'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 1),
	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000004' AND c.type = 'wishlist'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1),
	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000005' AND c.type = 'active'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 2),
	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000005' AND c.type = 'wishlist'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 1);

-- ==========================
-- product reviews
-- ==========================

INSERT INTO product_reviews (product_id, user_id, rating, comment)
VALUES
	((SELECT id FROM products WHERE name = 'Laptop Pro 14'), (SELECT id FROM users WHERE phone = '+79990000004'), 5, 'Excellent laptop for study and work.'),
	((SELECT id FROM products WHERE name = 'Wireless Mouse X'), (SELECT id FROM users WHERE phone = '+79990000005'), 4, 'Comfortable mouse, good battery life.'),
	((SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), (SELECT id FROM users WHERE phone = '+79990000004'), 5, 'Very useful dock, stable connection.');

COMMIT;