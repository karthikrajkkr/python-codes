-- Create Database (MySQL/PostgreSQL syntax)
CREATE DATABASE IF NOT EXISTS test_ecommerceordersordersorders;
USE test_ecommerce;

-- For PostgreSQL, use:
-- CREATE DATABASE test_ecommerce;
-- \c test_ecommerce;

-- Create Schema (PostgreSQL only - MySQL uses databases instead of schemas)
-- CREATE SCHEMA IF NOT EXISTS ecommerce_schema;
-- SET search_path TO ecommerce_schema;

-- =============================================
-- TABLE CREATION
-- =============================================

-- 1. Categories Table
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Products Table
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(200) NOT NULL,
    category_id INT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- 3. Customers Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Orders Table
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    shipping_address TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 5. Order Items Table (Junction table for orders and products)
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) AS (quantity * unit_price) STORED,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- =============================================
-- INSERT TEST DATA
-- =============================================

-- Insert Categories
INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Electronic devices and gadgets'),
('Clothing', 'Apparel and fashion items'),
('Books', 'Books and educational materials'),
('Home & Garden', 'Home improvement and gardening supplies'),
('Sports', 'Sports equipment and accessories');

-- Insert Products
INSERT INTO products (product_name, category_id, price, stock_quantity, description) VALUES
('Smartphone Pro Max', 1, 999.99, 50, 'Latest flagship smartphone with advanced features'),
('Wireless Headphones', 1, 199.99, 100, 'High-quality wireless headphones with noise cancellation'),
('Laptop Computer', 1, 1299.99, 25, 'Powerful laptop for work and gaming'),
('Cotton T-Shirt', 2, 29.99, 200, 'Comfortable 100% cotton t-shirt'),
('Denim Jeans', 2, 79.99, 150, 'Classic fit denim jeans'),
('Winter Jacket', 2, 149.99, 75, 'Warm winter jacket for cold weather'),
('Programming Cookbook', 3, 45.99, 80, 'Comprehensive guide to programming'),
('Science Fiction Novel', 3, 14.99, 120, 'Bestselling science fiction adventure'),
('Garden Hose', 4, 34.99, 60, '50-foot expandable garden hose'),
('Plant Fertilizer', 4, 19.99, 90, 'Organic plant fertilizer for healthy growth'),
('Tennis Racket', 5, 89.99, 40, 'Professional tennis racket for competitive play'),
('Running Shoes', 5, 129.99, 80, 'Lightweight running shoes with excellent support');

-- Insert Customers
INSERT INTO customers (first_name, last_name, email, phone, address, city, country) VALUES
('John', 'Doe', 'john.doe@email.com', '+1-555-0101', '123 Main St', 'New York', 'USA'),
('Jane', 'Smith', 'jane.smith@email.com', '+1-555-0102', '456 Oak Ave', 'Los Angeles', 'USA'),
('Mike', 'Johnson', 'mike.johnson@email.com', '+1-555-0103', '789 Pine Rd', 'Chicago', 'USA'),
('Sarah', 'Wilson', 'sarah.wilson@email.com', '+1-555-0104', '321 Elm St', 'Miami', 'USA'),
('David', 'Brown', 'david.brown@email.com', '+1-555-0105', '654 Maple Dr', 'Seattle', 'USA'),
('Emily', 'Davis', 'emily.davis@email.com', '+1-555-0106', '987 Cedar Ln', 'Boston', 'USA'),
('Chris', 'Miller', 'chris.miller@email.com', '+1-555-0107', '147 Birch Way', 'Denver', 'USA'),
('Lisa', 'Anderson', 'lisa.anderson@email.com', '+1-555-0108', '258 Spruce St', 'Portland', 'USA');

-- Insert Orders
INSERT INTO orders (customer_id, total_amount, status, shipping_address) VALUES
(1, 1199.98, 'delivered', '123 Main St, New York, USA'),
(2, 229.98, 'shipped', '456 Oak Ave, Los Angeles, USA'),
(3, 79.99, 'processing', '789 Pine Rd, Chicago, USA'),
(4, 164.98, 'pending', '321 Elm St, Miami, USA'),
(5, 1329.98, 'delivered', '654 Maple Dr, Seattle, USA'),
(6, 89.99, 'cancelled', '987 Cedar Ln, Boston, USA'),
(7, 349.97, 'shipped', '147 Birch Way, Denver, USA'),
(8, 54.98, 'delivered', '258 Spruce St, Portland, USA');

-- Insert Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
-- Order 1 (John Doe)
(1, 1, 1, 999.99),  -- Smartphone
(1, 2, 1, 199.99),  -- Wireless Headphones

-- Order 2 (Jane Smith)
(2, 4, 1, 29.99),   -- T-Shirt
(2, 2, 1, 199.99),  -- Wireless Headphones

-- Order 3 (Mike Johnson)
(3, 5, 1, 79.99),   -- Denim Jeans

-- Order 4 (Sarah Wilson)
(4, 6, 1, 149.99),  -- Winter Jacket
(4, 8, 1, 14.99),   -- Science Fiction Novel

-- Order 5 (David Brown)
(5, 3, 1, 1299.99), -- Laptop
(5, 4, 1, 29.99),   -- T-Shirt

-- Order 6 (Emily Davis) - Cancelled
(6, 11, 1, 89.99),  -- Tennis Racket

-- Order 7 (Chris Miller)
(7, 12, 1, 129.99), -- Running Shoes
(7, 7, 1, 45.99),   -- Programming Book
(7, 9, 1, 34.99),   -- Garden Hose
(7, 10, 4, 19.99),  -- Plant Fertilizer (4 units)

-- Order 8 (Lisa Anderson)
(8, 9, 1, 34.99),   -- Garden Hose
(8, 10, 1, 19.99);  -- Plant Fertilizer

-- =============================================
-- VERIFICATION QUERIES
-- =============================================

-- Check all tables have data
SELECT 'Categories' as table_name, COUNT(*) as record_count FROM categories
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Customers', COUNT(*) FROM customers
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items;

-- Sample join query to verify relationships
SELECT
    o.order_id,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.total_price,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id, oi.order_item_id;

-- Product inventory summary
SELECT
    cat.category_name,
    p.product_name,
    p.price,
    p.stock_quantity,
    CASE
        WHEN p.stock_quantity > 100 THEN 'High Stock'
        WHEN p.stock_quantity > 50 THEN 'Medium Stock'
        WHEN p.stock_quantity > 0 THEN 'Low Stock'
        ELSE 'Out of Stock'
    END as stock_status
FROM products p
JOIN categories cat ON p.category_id = cat.category_id
ORDER BY cat.category_name, p.product_name;