-- =========================
-- BASE DE DATOS: stockflow_db
-- =========================

CREATE DATABASE IF NOT EXISTS stockflow_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE stockflow_db;

-- =========================
-- TABLA: products
-- =========================

CREATE TABLE IF NOT EXISTS products (
    id             INT             NOT NULL AUTO_INCREMENT,
    name           VARCHAR(150)    NOT NULL,
    category       VARCHAR(100)    NOT NULL,
    stock          INT             NOT NULL DEFAULT 0,
    minimum_stock  INT             NOT NULL DEFAULT 1,
    price          DECIMAL(10, 2)  NOT NULL,
    created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    INDEX idx_category (category),
    INDEX idx_name     (name)
);

-- =========================
-- DATOS DE PRUEBA
-- =========================

INSERT INTO products (name, category, stock, minimum_stock, price) VALUES
    ('Baterías AAA x4',      'Baterias',   10,  5,  5000.00),
    ('Baterías AA x4',       'Baterias',    8,  5,  5500.00),
    ('Cargador USB-C 20W',   'Cargadores',  6,  3, 35000.00),
    ('Cargador Inalámbrico', 'Cargadores',  3,  2, 55000.00),
    ('Audífonos Bluetooth',  'Audifonos',   4,  2, 89000.00),
    ('Audífonos con cable',  'Audifonos',  12,  4, 25000.00);
