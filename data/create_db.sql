-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS pybooks_db;
USE pybooks_db;

-- Criar a tabela users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10,2) DEFAULT 0.00,
    join_date DATE NOT NULL,
    email VARCHAR(100),
    active BOOLEAN DEFAULT TRUE
);

-- Criar a tabela books
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    genre VARCHAR(100),
    status VARCHAR(50) DEFAULT 'to_read',
    added_at DATETIME
);