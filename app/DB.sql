CREATE TABLE IF NOT EXISTS users(
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMPZ NOT NULL,
    UNIQUE(user_email)
);

CREATE TABLE IF NOT EXISTS products(
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_details VARCHAR(200) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

