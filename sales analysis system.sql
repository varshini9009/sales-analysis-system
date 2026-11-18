--- creating database---
create database sales_db;
--- use database--
use sales_db;
--- creating tables---
create table products(
product_id int auto_increment primary key,
product_name varchar(100) not null,
price decimal(10,2)not null);

create table customers(
customer_id int auto_increment primary key,
customer_name varchar(100) not null,
email varchar(100)unique);

create table sales(
sale_id int auto_increment primary key,
customer_id int,
sale_date date not null,
foreign key(customer_id)references customers(customer_id));

create table sale_items(
sale_item_id int auto_increment primary key,
sale_id int,
product_id int,
quantity int not null,
price decimal(10,2)not null,
foreign key(sale_id)references sales(sale_id),
foreign key(product_id)references products(product_id));

INSERT INTO products (product_name, price) VALUES
('T-Shirt', 800),
('Jeans', 1500),
('Shirt', 1200),
('Dress', 2000),
('Jacket', 3000),
('Hoodie', 1800),
('Skirt', 1000),
('Sweater', 2200),
('Shoes', 2500),
('Sandals', 1200),
('Cap', 500),
('Handbag', 2000);

INSERT INTO customers (customer_name, email) VALUES
('Ravi', 'ravi@gmail.com'),
('Priya', 'priya@gmail.com'),
('Arun', 'arun@gmail.com'),
('Sneha', 'sneha@gmail.com'),
('Kiran', 'kiran@gmail.com'),
('Anjali', 'anjali@gmail.com'),
('Rahul', 'rahul@gmail.com'),
('Divya', 'divya@gmail.com'),
('Vijay', 'vijay@gmail.com'),
('Lakshmi', 'lakshmi@gmail.com');


INSERT INTO sales (customer_id, sale_date) VALUES
(1, '2026-07-10'),
(2, '2026-07-15'),
(3, '2026-08-01'),
(4, '2026-08-05'),
(5, '2026-08-12'),
(6, '2026-08-20'),
(7, '2026-09-02'),
(8, '2026-07-10'),
(9, '2026-07-15'),
(10, '2026-08-01'),
(1, '2026-08-10'),
(3, '2026-08-18');


INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES
(1, 1, 2, 800),
(1, 2, 1, 1500),

(2, 3, 2, 1200),
(2, 4, 1, 2000),

(3, 5, 1, 3000),
(3, 1, 3, 800),

(4, 6, 2, 1800),
(4, 7, 1, 1000),

(5, 8, 1, 2200),
(5, 9, 2, 2500),

(6, 10, 3, 1200),
(6, 11, 2, 500),

(7, 12, 1, 2000),
(7, 2, 2, 1500),

(8, 1, 1, 800),
(8, 3, 2, 1200),

(9, 4, 2, 2000),
(9, 5, 1, 3000),

(10, 6, 1, 1800),
(10, 9, 2, 2500),

(11, 7, 3, 1000),
(11, 10, 1, 1200),

(12, 11, 4, 500),
(12, 12, 2, 2000);