-- Создание таблиц
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT
);

CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT
);

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    region_id INTEGER,
    date DATE,
    amount DECIMAL,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);
