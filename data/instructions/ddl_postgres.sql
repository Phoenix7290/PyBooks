-- DDL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  

-- Tabela users
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    username    VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role        VARCHAR(50) NOT NULL,
    department  VARCHAR(50),
    salary      NUMERIC(10,2) DEFAULT 0.00,
    join_date   DATE NOT NULL,
    email       VARCHAR(100),
    active      BOOLEAN DEFAULT TRUE
);

CREATE TABLE books (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    genre       VARCHAR(100),
    status      VARCHAR(50) DEFAULT 'to_read',
    added_at    TIMESTAMP,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);