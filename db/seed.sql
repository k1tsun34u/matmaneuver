-- =====================================
-- seed.sql
-- Безопасное заполнение тестовыми данными
-- без жёсткой привязки к id = 1,2,3...
-- =====================================

-- ==========================
-- USERS
-- ==========================

INSERT INTO users (phone, email, full_name, password_hash)
VALUES
('+79990000001', 'ivan@example.com', 'Иван Петров', 'hash_ivan'),
('+79990000002', 'anna@example.com', 'Анна Смирнова', 'hash_anna'),
('+79990000003', 'sergey@example.com', 'Сергей Иванов', 'hash_sergey'),
('+79990000004', 'admin@example.com', 'Главный Администратор', 'hash_admin'),
('+79990000005', 'manager@example.com', 'Менеджер Заказов', 'hash_manager')
ON CONFLICT (email) DO NOTHING;


-- ==========================
-- EMPLOYEES
-- ==========================

INSERT INTO employees (user_id, hired_at)
SELECT id, CURRENT_DATE - INTERVAL '365 days'
FROM users
WHERE email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1 FROM employees e
	WHERE e.user_id = users.id
);

INSERT INTO employees (user_id, hired_at)
SELECT id, CURRENT_DATE - INTERVAL '180 days'
FROM users
WHERE email = 'manager@example.com'
AND NOT EXISTS (
	SELECT 1 FROM employees e
	WHERE e.user_id = users.id
);


-- ==========================
-- ROLES
-- ==========================

INSERT INTO roles (code, created_by)
SELECT 'super_admin', e.id
FROM employees e
JOIN users u ON u.id = e.user_id
WHERE u.email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1 FROM roles WHERE code = 'super_admin'
);

INSERT INTO roles (code, created_by)
SELECT 'order_manager', e.id
FROM employees e
JOIN users u ON u.id = e.user_id
WHERE u.email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1 FROM roles WHERE code = 'order_manager'
);

INSERT INTO roles (code, created_by)
SELECT 'warehouse', e.id
FROM employees e
JOIN users u ON u.id = e.user_id
WHERE u.email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1 FROM roles WHERE code = 'warehouse'
);


-- ==========================
-- PERMISSIONS
-- ==========================

INSERT INTO permissions (code, description)
VALUES
('manage_products', 'Управление товарами'),
('manage_orders', 'Управление заказами'),
('manage_inventory', 'Управление остатками'),
('view_users', 'Просмотр пользователей')
ON CONFLICT (code) DO NOTHING;


-- ==========================
-- EMPLOYEE ROLES
-- ==========================

INSERT INTO employee_roles (employee_id, role_id, created_by)
SELECT
	e.id,
	r.id,
	admin_emp.id
FROM employees e
JOIN users u ON u.id = e.user_id
JOIN roles r ON r.code = 'super_admin'
JOIN employees admin_emp ON admin_emp.id = r.created_by
WHERE u.email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1
	FROM employee_roles er
	WHERE er.employee_id = e.id
	AND er.role_id = r.id
);


-- ==========================
-- WAREHOUSES
-- ==========================

INSERT INTO warehouses (address, description, created_by)
SELECT
	'Москва, ул. Логистическая, 10',
	'Основной склад',
	e.id
FROM employees e
JOIN users u ON u.id = e.user_id
WHERE u.email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1 FROM warehouses
	WHERE address = 'Москва, ул. Логистическая, 10'
);


-- ==========================
-- PRODUCT CATEGORIES
-- ==========================

INSERT INTO product_categories (name, created_by)
SELECT
	'Смартфоны',
	e.id
FROM employees e
JOIN users u ON u.id = e.user_id
WHERE u.email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1 FROM product_categories
	WHERE name = 'Смартфоны'
);

INSERT INTO product_categories (name, created_by)
SELECT
	'Ноутбуки',
	e.id
FROM employees e
JOIN users u ON u.id = e.user_id
WHERE u.email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1 FROM product_categories
	WHERE name = 'Ноутбуки'
);


-- ==========================
-- PRODUCTS
-- ==========================

INSERT INTO products (
	product_category_id,
	name,
	description,
	price,
	created_by
)
SELECT
	pc.id,
	'iPhone 15',
	'Apple smartphone',
	89990.00,
	e.id
FROM product_categories pc
JOIN employees e ON TRUE
JOIN users u ON u.id = e.user_id
WHERE pc.name = 'Смартфоны'
AND u.email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1 FROM products
	WHERE name = 'iPhone 15'
);

INSERT INTO products (
	product_category_id,
	name,
	description,
	price,
	created_by
)
SELECT
	pc.id,
	'MacBook Air M3',
	'Apple laptop',
	129990.00,
	e.id
FROM product_categories pc
JOIN employees e ON TRUE
JOIN users u ON u.id = e.user_id
WHERE pc.name = 'Ноутбуки'
AND u.email = 'admin@example.com'
AND NOT EXISTS (
	SELECT 1 FROM products
	WHERE name = 'MacBook Air M3'
);


-- ==========================
-- ORDERS
-- ==========================

INSERT INTO orders (
	user_id,
	current_status,
	track_number,
	delivery_address
)
SELECT
	u.id,
	'confirmed',
	'TRACK123456',
	'Москва, ул. Пушкина, д. 1'
FROM users u
WHERE u.email = 'ivan@example.com'
AND NOT EXISTS (
	SELECT 1 FROM orders
	WHERE track_number = 'TRACK123456'
);


-- ==========================
-- ORDER ITEMS
-- ==========================

INSERT INTO order_items (
	order_id,
	product_id,
	quantity,
	price
)
SELECT
	o.id,
	p.id,
	1,
	89990.00
FROM orders o
JOIN products p ON p.name = 'iPhone 15'
WHERE o.track_number = 'TRACK123456'
AND NOT EXISTS (
	SELECT 1 FROM order_items oi
	WHERE oi.order_id = o.id
	AND oi.product_id = p.id
);


-- ==========================
-- REVIEWS
-- ==========================

INSERT INTO product_reviews (
	product_id,
	user_id,
	rating,
	comment
)
SELECT
	p.id,
	u.id,
	5,
	'Отличный товар, рекомендую'
FROM products p
JOIN users u ON u.email = 'ivan@example.com'
WHERE p.name = 'iPhone 15'
AND NOT EXISTS (
	SELECT 1
	FROM product_reviews pr
	WHERE pr.product_id = p.id
	AND pr.user_id = u.id
);


-- ==========================
-- FAVORITES
-- ==========================

INSERT INTO user_favorite_products (
	user_id,
	product_id
)
SELECT
	u.id,
	p.id
FROM users u
JOIN products p ON p.name = 'MacBook Air M3'
WHERE u.email = 'ivan@example.com'
AND NOT EXISTS (
	SELECT 1
	FROM user_favorite_products f
	WHERE f.user_id = u.id
	AND f.product_id = p.id
);