CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(email)
);

CREATE TABLE IF NOT EXISTS products(
    id SERIAL PRIMARY KEY,
    sku VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    details VARCHAR(200) NOT NULL,
    price INT, 
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(sku)
);

CREATE TABLE IF NOT EXISTS jobs(
    job_id uuid PRIMARY KEY,
    status VARCHAR(100) NOT NULL,
    triggered_by INT,
    triggered_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
