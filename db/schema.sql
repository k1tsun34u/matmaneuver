-- //////////////////////////
-- Таблицы
-- //////////////////////////

CREATE TABLE users (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	phone VARCHAR(32) UNIQUE NOT NULL,
	email VARCHAR(256) UNIQUE,
	full_name TEXT NOT NULL,
	password_hash TEXT NOT NULL,

	blocked_by BIGINT REFERENCES employees(id),
	blocked_at TIMESTAMPTZ,

	deleted_by BIGINT REFERENCES employees(id),
	deleted_at TIMESTAMPTZ,
	
	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==========================
-- Сотрудники, их роли (НЕ ДОЛЖНОСТИ!) и возможности
-- ==========================

CREATE TABLE employees (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	user_id BIGINT UNIQUE NOT NULL REFERENCES users(id),

	hired_by BIGINT REFERENCES employees(id),
	hired_at DATE NOT NULL,

	fired_by BIGINT REFERENCES employees(id),
	fired_at TIMESTAMPTZ,
	
	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

/*
'super_admin' - главный админ: всё
'admin' - обычный админ:
	+ управление товарами
	+ управление заказами
	+ модерация отзывов
	- управление системой безопасности
	- выдача ролей
'order_manager' - менеджер заказов:
	+ просмотр заказов
	+ изменение статусов заказов
	+ взаимодействие с клиентом
	+ оформление возвратов
'warehouse' - кладовщик:
	+ изменение остатков товаров
	+ подтверждение отправки товаров
	+ просмотр склада
	- изменение цен
	- удаление товаров
'content_manager' - контентщик:
	+ изменение характеристик, описания и фото товаров
	- изменение цен
	- управление заказами
'support' - поддержка:
	+ просмотр пользователей
	+ помощь с восстановлением учёток
	+ реагирование на жалобы
	- управление товарами
*/
CREATE TABLE roles (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	code TEXT UNIQUE NOT NULL,
	
	is_system BOOLEAN NOT NULL,

	deactivated_by BIGINT REFERENCES employees(id),
	deactivated_at TIMESTAMPTZ DEFAULT NULL,

	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE permissions (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	code TEXT UNIQUE NOT NULL,
	description TEXT,

	is_system BOOLEAN NOT NULL,

	deactivated_by BIGINT REFERENCES employees(id),
	deactivated_at TIMESTAMPTZ DEFAULT NULL,

	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE role_permissions (
	role_id BIGINT NOT NULL REFERENCES roles(id),
	permission_id BIGINT NOT NULL REFERENCES permissions(id),

	assigned_by BIGINT REFERENCES employees(id),
	assigned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE employee_roles (
	employee_id BIGINT NOT NULL REFERENCES employees(id),
	role_id BIGINT NOT NULL REFERENCES roles(id),

	assigned_by BIGINT REFERENCES employees(id),
	assigned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	PRIMARY KEY (employee_id, role_id)
);

-- ==========================
-- Склады и товары
-- ==========================

CREATE TABLE warehouses (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	address TEXT UNIQUE NOT NULL,
	description TEXT,

	deleted_by BIGINT REFERENCES employees(id),
	deleted_at TIMESTAMPTZ DEFAULT NULL,
	
	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE categories (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	parent_category_id BIGINT REFERENCES categories(id),
	name TEXT UNIQUE NOT NULL,
	
	deactivated_by BIGINT REFERENCES employees(id),
	deactivated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	
	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Товары
CREATE TABLE products (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name TEXT NOT NULL,
	description TEXT,
	price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
	
	deleted_by BIGINT REFERENCES users(id),
	deleted_at TIMESTAMPTZ DEFAULT NULL,

	created_by BIGINT REFERENCES users(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE product_categories (
	product_id BIGINT NOT NULL REFERENCES products(id),
	category_id BIGINT NOT NULL REFERENCES categories(id),

	assigned_by BIGINT REFERENCES users(id),
	assigned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	PRIMARY KEY (product_id, category_id)
);

CREATE TABLE product_images (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	product_id BIGINT NOT NULL REFERENCES products(id),
	storage_key TEXT NOT NULL,

	created_by BIGINT REFERENCES users(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Остатки на складе
CREATE TABLE warehouse_products (
	product_id BIGINT NOT NULL REFERENCES products(id),
	warehouse_id BIGINT NOT NULL REFERENCES warehouses(id),
	quantity INT NOT NULL CHECK (quantity >= 0) DEFAULT 0,
	reserved_quantity INT NOT NULL CHECK (reserved_quantity >= 0) DEFAULT 0,
	
	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	PRIMARY KEY (product_id, warehouse_id),
	CHECK (quantity >= 0),
	CHECK (reserved_quantity >= 0),
	CHECK (reserved_quantity <= quantity)
);

-- ==========================
-- Поставщики и поставки
-- ==========================

-- Поставщики
CREATE TABLE suppliers (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name TEXT NOT NULL,
	phone VARCHAR(32) UNIQUE NOT NULL,
	email VARCHAR(256) UNIQUE,
	address TEXT,

	deactivated_by BIGINT REFERENCES employees(id),
	deactivated_at TIMESTAMPTZ DEFAULT NULL,

	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TYPE supply_status AS ENUM(
	'created',
	'confirmed',
	'in_transit',
	'delivered',
	'cancelled'
);

-- Поставки
CREATE TABLE supplies (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	supplier_id BIGINT NOT NULL REFERENCES suppliers(id),
	warehouse_id BIGINT NOT NULL REFERENCES warehouses(id),
	current_status supply_status NOT NULL DEFAULT 'created',
	planned_delivery_date DATE NOT NULL,

	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Состав поставок
CREATE TABLE supply_items (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	supply_id BIGINT NOT NULL REFERENCES supplies(id),
	product_id BIGINT NOT NULL REFERENCES products(id),
	quantity INT NOT NULL CHECK (quantity > 0),
	price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
	UNIQUE (supply_id, product_id)
);

CREATE TABLE supply_status_history (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	supply_id BIGINT NOT NULL REFERENCES supplies(id),
	status supply_status NOT NULL,

	changed_by BIGINT REFERENCES employees(id),
	changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==========================
-- Заказы
-- ==========================

CREATE TYPE order_status AS ENUM(
	'created',
	'confirmed',
	'in_transit',
	'delivered',
	'cancelled'
);

CREATE TABLE orders (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	user_id BIGINT NOT NULL REFERENCES users(id),
	current_status order_status NOT NULL DEFAULT 'created',
	track_number TEXT UNIQUE,
	delivery_address TEXT NOT NULL,

	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_id BIGINT NOT NULL REFERENCES orders(id),
	product_id BIGINT NOT NULL REFERENCES products(id),
	quantity INT NOT NULL CHECK (quantity > 0),
	price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
	UNIQUE (order_id, product_id)
);

CREATE TABLE order_status_history (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_id BIGINT NOT NULL REFERENCES orders(id),
	status order_status NOT NULL,

	changed_by BIGINT REFERENCES employees(id),
	changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==========================
-- Возвраты
-- ==========================

CREATE TYPE return_status AS ENUM (
	'created',
	'confirmed',
	'in_transit',
	'finished'
);

CREATE TABLE returns (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_id BIGINT NOT NULL REFERENCES orders(id),
	reason TEXT NOT NULL,
	current_status return_status NOT NULL DEFAULT 'created',

	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE return_items (
	return_id BIGINT NOT NULL REFERENCES returns(id),
	order_item_id BIGINT NOT NULL REFERENCES order_items(id),
	quantity INT NOT NULL CHECK (quantity > 0),
	price_at_return NUMERIC(10, 2) NOT NULL CHECK (price_at_return >= 0),
	PRIMARY KEY (return_id, order_item_id)
);

CREATE TABLE return_status_history (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	return_id BIGINT NOT NULL REFERENCES returns(id),
	status return_status NOT NULL,
	
	changed_by BIGINT REFERENCES employees(id),
	changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==========================
-- Списания
-- ==========================

CREATE TYPE write_off_status AS ENUM (
	'created',
	'in_progress',
	'finished'
);

CREATE TABLE write_offs (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	employee_id BIGINT NOT NULL REFERENCES employees(id),
	reason TEXT NOT NULL,
	current_status write_off_status NOT NULL DEFAULT 'created',

	created_by BIGINT REFERENCES employees(id),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE write_off_items (
	write_off_id BIGINT NOT NULL REFERENCES write_offs(id),
	product_id BIGINT NOT NULL REFERENCES products(id),
	quantity INT NOT NULL CHECK (quantity > 0),
	PRIMARY KEY (write_off_id, product_id)
);

CREATE TABLE write_off_status_history (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	write_off_id BIGINT NOT NULL REFERENCES write_offs(id),
	status write_off_status NOT NULL,
	
	changed_by BIGINT REFERENCES employees(id),
	changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==========================
-- Доставка заказов
-- ==========================

CREATE TYPE transport_type AS ENUM (
	'land',
	'air',
	'sea'
);

CREATE TABLE order_deliveries (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_id BIGINT NOT NULL REFERENCES orders(id),
	total_price NUMERIC(10, 2) NOT NULL CHECK (total_price > 0),

	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_delivery_segments (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_delivery_id BIGINT NOT NULL REFERENCES order_deliveries(id),
	sequence_number INT NOT NULL CHECK (sequence_number > 0),
	transport_type transport_type NOT NULL,
	address_from TEXT NOT NULL,
	address_to TEXT NOT NULL,
	price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
	UNIQUE (order_delivery_id, sequence_number)
);

-- ==========================
-- Платежи
-- ==========================

CREATE TYPE payment_method AS ENUM (
	'cash',
	'card',
	'sbp'				-- СБП
);

CREATE TABLE order_payments (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_id BIGINT NOT NULL REFERENCES orders(id),
	amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
	payment_method payment_method NOT NULL,

	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==========================
-- Корзина
-- ==========================

CREATE TABLE carts (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	user_id BIGINT UNIQUE NOT NULL REFERENCES users(id),
	
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE cart_items (
	cart_id BIGINT NOT NULL REFERENCES carts(id),
	product_id BIGINT NOT NULL REFERENCES products(id),
	quantity INT NOT NULL CHECK (quantity > 0),
	
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	PRIMARY KEY (cart_id, product_id)
);

-- ==========================
-- Отзывы
-- ==========================

CREATE TABLE product_reviews (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	product_id BIGINT NOT NULL REFERENCES products(id),
	user_id BIGINT NOT NULL REFERENCES users(id),
	rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
	comment TEXT,

	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	UNIQUE (product_id, user_id)
);

-- ==========================
-- Любимые товары пользователя
-- ==========================

CREATE TABLE user_favorite_products (
	user_id BIGINT NOT NULL REFERENCES users(id),
	product_id BIGINT NOT NULL REFERENCES products(id),

	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	PRIMARY KEY (user_id, product_id)
);

-- //////////////////////////
-- Индексы (на внешние ключи
-- полей фильтрации,
-- сортировки,
-- часто исп-ые
-- поиск-ые поля)
-- для уменьшения кол-ва
-- поиска по всей таблице,
-- ускорения JOIN-операций
-- //////////////////////////

CREATE INDEX idx_users_deleted_at ON users(deleted_at);

CREATE INDEX idx_employees_created_by ON employees(created_by);

CREATE INDEX idx_products_is_active ON products(is_active);

CREATE INDEX idx_product_images_product_id ON product_images(product_id);

CREATE INDEX idx_warehouse_products_warehouse_id ON warehouse_products(warehouse_id);

CREATE INDEX idx_supplies_supplier_id ON supplies(supplier_id);
CREATE INDEX idx_supplies_warehouse_id ON supplies(warehouse_id);
CREATE INDEX idx_supplies_status ON supplies(current_status);
CREATE INDEX idx_supplies_created_at ON supplies(created_at);

CREATE INDEX idx_supply_items_supply_id ON supply_items(supply_id);
CREATE INDEX idx_supply_items_product_id ON supply_items(product_id);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(current_status);
CREATE INDEX idx_orders_created_at ON orders(created_at);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

CREATE INDEX idx_returns_order_id ON returns(order_id);
CREATE INDEX idx_returns_status ON returns(current_status);

CREATE INDEX idx_order_payments_order_id ON order_payments(order_id);

CREATE INDEX idx_reviews_product_id ON product_reviews(product_id);
CREATE INDEX idx_reviews_user_id ON product_reviews(user_id);

CREATE INDEX idx_cart_items_product_id ON cart_items(product_id);

CREATE INDEX idx_favorites_product_id ON user_favorite_products(product_id);

CREATE INDEX idx_order_status_history_order_id ON order_status_history(order_id);
CREATE INDEX idx_supply_status_history_supply_id ON supply_status_history(supply_id);
CREATE INDEX idx_return_status_history_return_id ON return_status_history(return_id);
CREATE INDEX idx_write_off_status_history_write_off_id ON write_off_status_history(write_off_id);

