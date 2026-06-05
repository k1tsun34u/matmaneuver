BEGIN;

-- ==========================
-- users / employees
-- ==========================

INSERT INTO users (phone, email, full_name, password_hash, blocked_by, blocked_at, deleted_by, deleted_at, created_by)
VALUES ('71111111111', 'pse@mail.ru', 'Пилясов С Э', '$2b$12$jHB0vTDGjGAIeRi/8pn/JuxLK1cLaaDCo.IdpV3AWp00yQpGtrrti', NULL, NULL, NULL, NULL, NULL);

INSERT INTO employees (user_id, hired_by, hired_at, fired_by, fired_at, created_by)
VALUES ((SELECT id FROM users WHERE phone = '71111111111'), NULL, NOW() - INTERVAL '39 days', NULL, NULL, NULL);

-- ==========================
-- roles / permissions / mappings
-- ==========================

INSERT INTO roles (code, is_system, deactivated_by, created_by)
VALUES
	('SUPER_ADMIN', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111')));

INSERT INTO permissions (code, description, is_system, deactivated_by, created_by)
VALUES
	('CREATE_USER', 'Permission: create_user', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('BLOCK_USER', 'Permission: block_user', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('UNBLOCK_USER', 'Permission: unblock_user', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DELETE_USER', 'Permission: delete_user', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_EMPLOYEE', 'Permission: create_employee', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('HIRE', 'Permission: hire', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('FIRE', 'Permission: fire', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_PERMISSION', 'Permission: create_permission', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('ASSIGN_PERMISSION', 'Permission: assign_permission', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('UNASSIGN_PERMISSION', 'Permission: unassign_permission', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DEACTIVATE_PERMISSION', 'Permission: deactivate_permission', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('SET_PERMISSION_DESCRIPTION', 'Permission: set_permission_description', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_ROLE', 'Permission: create_role', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DEACTIVATE_ROLE', 'Permission: deactivate_role', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('ASSIGN_ROLE', 'Permission: assign_role', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('UNASSIGN_ROLE', 'Permission: unassign_role', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_CATEGORY', 'Permission: create_category', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DEACTIVATE_CATEGORY', 'Permission: deactivate_category', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('SET_CATEGORY_PARENT', 'Permission: set_category_parent', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_ORDER_FULFILLMENT', 'Permission: create_order_fulfillment', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('CREATE_ORDER_FULFILLMENT_ITEM', 'Permission: create_order_fulfillment_item', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),

	('CREATE_WAREHOUSE', 'Permission: create_warehouse', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DELETE_WAREHOUSE', 'Permission: delete_warehouse', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('SET_WAREHOUSE_DESCRIPTION', 'Permission: set_warehouse_description', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('ADD_WAREHOUSE_PRODUCT', 'Permission: add_warehouse_product', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DELETE_WAREHOUSE_PRODUCT', 'Permission: delete_warehouse_product', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_PRODUCT', 'Permission: create_product', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DELETE_PRODUCT', 'Permission: delete_product', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('SET_PRODUCT_PRICE', 'Permission: set_product_price', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('SET_PRODUCT_DESCRIPTION', 'Permission: set_product_description', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('ASSIGN_PRODUCT_CATEGORY', 'Permission: assign_product_category', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('UNASSIGN_PRODUCT_CATEGORY', 'Permission: unassign_product_category', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('CREATE_PRODUCT_IMAGE', 'Permission: create_product_image', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DELETE_PRODUCT_IMAGE', 'Permission: delete_product_image', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_SUPPLIER', 'Permission: create_supplier', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DEACTIVATE_SUPPLIER', 'Permission: deactivate_supplier', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('SET_SUPPLIER_FIELDS', 'Permission: set_supplier_fields', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_SUPPLY', 'Permission: create_supply', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('SET_SUPPLY_STATUS', 'Permission: set_supply_status', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_SUPPLY_ITEM', 'Permission: create_supply_item', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DELETE_SUPPLY_ITEM', 'Permission: delete_supply_item', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('SET_ORDER_STATUS', 'Permission: set_order_status', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_WRITE_OFF', 'Permission: create_write_off', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DELETE_WRITE_OFF', 'Permission: delete_write_off', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('CREATE_WRITE_OFF_ITEM', 'Permission: create_write_off_item', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	('DELETE_WRITE_OFF_ITEM', 'Permission: delete_write_off_item', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
	('DELETE_PRODUCT_REVIEW', 'Permission: delete_product_review', TRUE, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111')));

INSERT INTO role_permissions (role_id, permission_id, assigned_by)
SELECT
	(SELECT id FROM roles WHERE code = 'SUPER_ADMIN'),
	p.id,
	(SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))
FROM permissions p;

INSERT INTO employee_roles (employee_id, role_id, assigned_by)
VALUES ((SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111')), (SELECT id FROM roles WHERE code = 'SUPER_ADMIN'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111')));

-- ==========================
-- warehouses / categories / products
-- ==========================

-- INSERT INTO warehouses (address, description, deleted_by, created_by)
-- VALUES
-- 	('г. Москва, 1-ая Дубровская улица, д. 20', 'Главный склад', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('г. Москва, 1-ая Дубровская улица, д. 19', NULL, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('г. Москва, 1-ая Дубровская улица, д. 18', NULL, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('г. Москва, 1-ая Дубровская улица, д. 17', NULL, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('г. Москва, ул. Пушкина, д. Колотушкина', NULL, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),

-- INSERT INTO categories (parent_category_id, name, deactivated_by, created_by)
-- VALUES
-- 	(NULL, 'Дерево', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	(NULL, 'Металл', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	(NULL, 'Мебель', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111')));

-- INSERT INTO products (name, description, price, deleted_by, created_by)
-- VALUES
-- 	('Фанера 300x100x1', 'Фанера [1] (длина: 300см, ширина: 100см, высота: 1см)', 1007.99, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Фанера 200x100x1', 'Фанера [2]', 864.49, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Фанера 120x200x2', 'Фанера [3]', 599.99, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Фанера 500x300x1', 'Фанера [4]', 1799.00, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('ДСП 300x100x1', 'ДСП [1] (длина: 300см, ширина: 100см, высота: 1см)', 1007.99, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('ДСП 200x100x1', 'ДСП [2]', 864.49, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('ДСП 120x200x2', 'ДСП [3]', 599.99, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('ДСП 500x300x1', 'ДСП [4]', 1799.00, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
-- 	('Сталь Ст0 500x500', 'Сталь [1]', 20000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Сталь Ст2кп 500x500', 'СТаль [2]', 21000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Сталь Ст3кп 500x500', 'СТаль [3]', 22000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Сталь Ст4кп 500x500', 'СТаль [4]', 23000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
-- 	('Кресло офисное кожаное серое', 'Кресло [1]', 5000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Кресло офисное кожаное белое', 'Кресло [2]', 5000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Кресло офисное кожаное синее', 'Кресло [3]', 5000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Кресло офисное кожаное бордовое', 'Кресло [4]', 5000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Кресло офисное кожаное красное', 'Кресло [5]', 5000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Табурет чёрный', 'Табурет [1]', 3000, NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),

-- INSERT INTO product_categories (product_id, category_id, assigned_by)
-- VALUES
-- 	((SELECT id FROM products WHERE name = 'Фанера 300x100x1'), (SELECT id FROM categories WHERE name = 'Дерево'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Фанера 200x100x1'), (SELECT id FROM categories WHERE name = 'Дерево'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Фанера 120x200x2'), (SELECT id FROM categories WHERE name = 'Дерево'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Фанера 500x300x1'), (SELECT id FROM categories WHERE name = 'Дерево'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'ДСП 300x100x1'), (SELECT id FROM categories WHERE name = 'Дерево'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'ДСП 200x100x1'), (SELECT id FROM categories WHERE name = 'Дерево'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'ДСП 120x200x2'), (SELECT id FROM categories WHERE name = 'Дерево'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'ДСП 500x300x1'), (SELECT id FROM categories WHERE name = 'Дерево'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
-- 	((SELECT id FROM products WHERE name = 'Сталь Ст0 500x500'), (SELECT id FROM categories WHERE name = 'Металл'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Сталь Ст2кп 500x500'), (SELECT id FROM categories WHERE name = 'Металл'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Сталь Ст3кп 500x500'), (SELECT id FROM categories WHERE name = 'Металл'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Сталь Ст4кп 500x500'), (SELECT id FROM categories WHERE name = 'Металл'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
-- 	((SELECT id FROM products WHERE name = 'Кресло офисное кожаное серое'), (SELECT id FROM categories WHERE name = 'Мебель'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Кресло офисное кожаное белое'), (SELECT id FROM categories WHERE name = 'Мебель'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Кресло офисное кожаное синее'), (SELECT id FROM categories WHERE name = 'Мебель'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Кресло офисное кожаное бордовое'), (SELECT id FROM categories WHERE name = 'Мебель'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Кресло офисное кожаное красное'), (SELECT id FROM categories WHERE name = 'Мебель'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Табурет чёрный'), (SELECT id FROM categories WHERE name = 'Мебель'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
	
-- INSERT INTO product_images (product_id, storage_key, created_by)
-- VALUES
-- 	((SELECT id FROM products WHERE name = 'Laptop Pro 14'), 'products/1/main.jpg', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'Wireless Mouse X'), 'products/2/main.jpg', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 'products/3/main.jpg', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111')));

-- INSERT INTO warehouse_products (product_id, warehouse_id, created_by)
-- VALUES
-- 	((SELECT id FROM products WHERE name = 'Laptop Pro 14'), (SELECT id FROM warehouses WHERE address = '123 North St, City A'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT id FROM products WHERE name = 'Wireless Mouse X'), (SELECT id FROM warehouses WHERE address = '123 North St, City A'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), (SELECT id FROM warehouses WHERE address = '123 North St, City A'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT id FROM products WHERE name = 'Laptop Pro 14'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT id FROM products WHERE name = 'Wireless Mouse X'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'), (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002')));

-- -- ==========================
-- -- suppliers / supplies
-- -- ==========================

-- INSERT INTO suppliers (full_name, phone, email, address, deactivated_by, created_by)
-- VALUES
-- 	('Tech Source LLC', '+78000000001', 'sales@techsource.local', 'Supplier Ave 10', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	('Parts Hub Inc', '+78000000002', 'hello@partshub.local', 'Industrial Rd 7', NULL, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111')));

-- INSERT INTO supplies (supplier_id, warehouse_id, planned_delivery_date, created_by)
-- VALUES
-- 	((SELECT id FROM suppliers WHERE phone = '+78000000001'), (SELECT id FROM warehouses WHERE address = '123 North St, City A'), CURRENT_DATE - 8, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT id FROM suppliers WHERE phone = '+78000000002'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'), CURRENT_DATE + 2, (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002')));

-- UPDATE supplies
-- SET current_status = 'delivered'
-- WHERE supplier_id = (SELECT id FROM suppliers WHERE phone = '+78000000001');

-- UPDATE supplies
-- SET current_status = 'in_transit'
-- WHERE supplier_id = (SELECT id FROM suppliers WHERE phone = '+78000000002');

-- INSERT INTO supply_items (supply_id, product_id, quantity, price)
-- VALUES
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 5, 1300.00),
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 50, 35.00),
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000002'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 20, 80.00);

-- INSERT INTO supply_status_history (supply_id, status, changed_by)
-- VALUES
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), 'confirmed', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), 'in_transit', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000001'), 'delivered', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000002'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000002'), 'confirmed', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '71111111111'))),
-- 	((SELECT s.id FROM supplies s JOIN suppliers sp ON sp.id = s.supplier_id WHERE sp.phone = '+78000000002'), 'in_transit', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002')));

-- -- ==========================
-- -- orders / order history / fulfillment / payments
-- -- ==========================

-- INSERT INTO orders (track_number, delivery_address, created_by)
-- VALUES
-- 	('TRK-2026-0001', 'Client Street 11, Apt 5', (SELECT id FROM users WHERE phone = '+79990000004')),
-- 	('TRK-2026-0002', 'Client Avenue 99, Apt 12', (SELECT id FROM users WHERE phone = '+79990000005')),
-- 	('TRK-2026-0003', 'Green Road 3, Apt 8', (SELECT id FROM users WHERE phone = '+79990000004'));

-- UPDATE orders SET current_status = 'confirmed' WHERE track_number = 'TRK-2026-0001';
-- UPDATE orders SET current_status = 'in_transit' WHERE track_number = 'TRK-2026-0002';

-- INSERT INTO order_items (order_id, product_id, quantity, price)
-- VALUES
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 1, 1599.99),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 2, 49.90),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1, 119.00),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 1, 49.90),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0003'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 1, 49.90);

-- INSERT INTO order_status_history (order_id, status, changed_by)
-- VALUES
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003'))),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), 'confirmed', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003'))),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003'))),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), 'confirmed', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003'))),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), 'in_transit', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0003'), 'created', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000003')));

-- INSERT INTO order_fulfillments (order_id, warehouse_id)
-- VALUES
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), (SELECT id FROM warehouses WHERE address = '123 North St, City A')),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), (SELECT id FROM warehouses WHERE address = '456 East St, City B'));

-- INSERT INTO order_fulfillment_items (order_fulfillment_id, product_id, quantity, price)
-- VALUES
-- 	((SELECT ofl.id FROM order_fulfillments ofl JOIN orders o ON o.id = ofl.order_id WHERE o.track_number = 'TRK-2026-0001'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 1, 1599.99),
-- 	((SELECT ofl.id FROM order_fulfillments ofl JOIN orders o ON o.id = ofl.order_id WHERE o.track_number = 'TRK-2026-0001'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 2, 49.90),
-- 	((SELECT ofl.id FROM order_fulfillments ofl JOIN orders o ON o.id = ofl.order_id WHERE o.track_number = 'TRK-2026-0002'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1, 119.00),
-- 	((SELECT ofl.id FROM order_fulfillments ofl JOIN orders o ON o.id = ofl.order_id WHERE o.track_number = 'TRK-2026-0002'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 1, 49.90);

-- INSERT INTO order_payments (order_id, amount, payment_method)
-- VALUES
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0001'), 1699.79, 'card'),
-- 	((SELECT id FROM orders WHERE track_number = 'TRK-2026-0002'), 168.90, 'sbp');

-- -- ==========================
-- -- write-offs
-- -- ==========================

-- INSERT INTO write_offs (warehouse_id, comment, created_by)
-- VALUES
-- 	((SELECT id FROM warehouses WHERE address = '123 North St, City A'), 'Packaging damage during handling', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002'))),
-- 	((SELECT id FROM warehouses WHERE address = '456 East St, City B'), 'Count mismatch found in cycle check', (SELECT id FROM employees WHERE user_id = (SELECT id FROM users WHERE phone = '+79990000002')));

-- UPDATE write_offs
-- SET reason = 'damaged'
-- WHERE warehouse_id = (SELECT id FROM warehouses WHERE address = '123 North St, City A');

-- UPDATE write_offs
-- SET reason = 'inventory_mismatch'
-- WHERE warehouse_id = (SELECT id FROM warehouses WHERE address = '456 East St, City B');

-- INSERT INTO write_off_items (write_off_id, product_id, quantity, price)
-- VALUES
-- 	((SELECT wo.id FROM write_offs wo JOIN warehouses w ON w.id = wo.warehouse_id WHERE w.address = '123 North St, City A'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 3, 35.00),
-- 	((SELECT wo.id FROM write_offs wo JOIN warehouses w ON w.id = wo.warehouse_id WHERE w.address = '456 East St, City B'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1, 80.00);

-- -- ==========================
-- -- carts / cart items
-- -- ==========================

INSERT INTO carts (user_id, type)
VALUES
	((SELECT id FROM users WHERE phone = '71111111111'), 'ACTIVE'),
	((SELECT id FROM users WHERE phone = '71111111111'), 'WISHLIST');

-- INSERT INTO carts (user_id, type)
-- VALUES
-- 	((SELECT id FROM users WHERE phone = '+79990000004'), 'ACTIVE'),
-- 	((SELECT id FROM users WHERE phone = '+79990000004'), 'WISHLIST'),
-- 	((SELECT id FROM users WHERE phone = '+79990000005'), 'ACTIVE'),
-- 	((SELECT id FROM users WHERE phone = '+79990000005'), 'WISHLIST');

-- INSERT INTO cart_items (cart_id, product_id, quantity)
-- VALUES
-- 	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000004' AND c.type = 'ACTIVE'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1),
-- 	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000004' AND c.type = 'WISHLIST'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 1),
-- 	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000004' AND c.type = 'WISHLIST'), (SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), 1),
-- 	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000005' AND c.type = 'ACTIVE'), (SELECT id FROM products WHERE name = 'Wireless Mouse X'), 2),
-- 	((SELECT c.id FROM carts c JOIN users u ON u.id = c.user_id WHERE u.phone = '+79990000005' AND c.type = 'WISHLIST'), (SELECT id FROM products WHERE name = 'Laptop Pro 14'), 1);

-- -- ==========================
-- -- product reviews
-- -- ==========================

-- INSERT INTO product_reviews (product_id, user_id, rating, comment)
-- VALUES
-- 	((SELECT id FROM products WHERE name = 'Laptop Pro 14'), (SELECT id FROM users WHERE phone = '+79990000004'), 5, 'Excellent laptop for study and work.'),
-- 	((SELECT id FROM products WHERE name = 'Wireless Mouse X'), (SELECT id FROM users WHERE phone = '+79990000005'), 4, 'Comfortable mouse, good battery life.'),
-- 	((SELECT id FROM products WHERE name = 'USB-C Dock 9in1'), (SELECT id FROM users WHERE phone = '+79990000004'), 5, 'Very useful dock, stable connection.');

COMMIT;