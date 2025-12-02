-- 1. metadados das páginas raspadas
CREATE TABLE scraped_pages (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    title_extracted VARCHAR(255),
    scraped_at TIMESTAMP DEFAULT NOW(),
    status_code INTEGER,
    success BOOLEAN DEFAULT FALSE,
    error_message TEXT
);

-- 2. erros detalhados (terceira tabela exigida no TP)
CREATE TABLE scraping_errors (
    id SERIAL PRIMARY KEY,
    page_id INTEGER REFERENCES scraped_pages(id) ON DELETE CASCADE,
    error_type VARCHAR(100),
    error_detail TEXT,
    occurred_at TIMESTAMP DEFAULT NOW()
);

-- 3. (opcional) autores extraídos
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL
);

-- Relacionamento muitos-para-muitos (se quiser ir além)
CREATE TABLE book_authors (
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    author_id INTEGER REFERENCES authors(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);