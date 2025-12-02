import requests
from bs4 import BeautifulSoup
import re
import psycopg2
from datetime import datetime
import time
import logging

# Config do log
logging.basicConfig(filename='tp5/scraped_books.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Conexão com seu banco atual
conn = psycopg2.connect(
    host="localhost",
    database="pybooks_db",
    user="postgres",
    password=""
)
cur = conn.cursor()

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_genre(soup):
    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return "Fiction"
    for tr in infobox.find_all("tr"):
        th = tr.find("th")
        if th and "Gênero" in th.get_text():
            td = tr.find("td")
            return clean_text(td.get_text()) if td else "Fiction"
    return "Fiction"

def scrape_book(url):
    headers = {'User-Agent': 'PyBooks-Scraper/1.0 (Educational Project)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find("h1", class_="firstHeading").get_text()
        
        # Primeiro parágrafo da introdução
        intro = soup.find("div", class_="mw-content-ltr")
        desc = ""
        for p in intro.find_all("p"):
            if p.get_text(strip=True):
                desc = clean_text(p.get_text())
                break
        
        genre = extract_genre(soup)

        # Insere na tabela books (evitando duplicatas por título)
        cur.execute("""
            INSERT INTO books (title, description, genre, status, added_at, user_id)
            VALUES (%s, %s, %s, 'to_read', NOW(), 1)
            ON CONFLICT (id) DO NOTHING
            RETURNING id
        """, (title, desc[:500], genre))
        
        book_id = cur.fetchone()
        success = book_id is not None
        
        # Registra metadados da página
        cur.execute("""
            INSERT INTO scraped_pages (url, title_extracted, status_code, success)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE SET
                scraped_at = NOW(),
                status_code = EXCLUDED.status_code,
                success = EXCLUDED.success
        """, (url, title, response.status_code, success))
        
        if success:
            logging.info(f"SUCESSO | {title} | {url}")
        else:
            logging.warning(f"DUPLICADO | {title} | {url}")
            
    except Exception as e:
        error_msg = str(e)[:500]
        logging.error(f"FALHA | {url} | {error_msg}")
        
        cur.execute("""
            INSERT INTO scraped_pages (url, status_code, success, error_message)
            VALUES (%s, %s, false, %s)
            ON CONFLICT (url) DO UPDATE SET
                scraped_at = NOW(), error_message = EXCLUDED.error_message
        """, (url, getattr(e, 'response', None).status_code if hasattr(e, 'response') else None, error_msg))
        
        cur.execute("""
            INSERT INTO scraping_errors (page_id, error_type, error_detail)
            VALUES (
                (SELECT id FROM scraped_pages WHERE url = %s),
                %s, %s
            )
        """, (url, type(e).__name__, error_msg))
    
    conn.commit()
    time.sleep(1)  # ser educado com a Wikipedia

# Lista de URLs (pode colocar em urls_livros.txt também)
URLS = [
    "https://pt.wikipedia.org/wiki/O_Pequeno_Príncipe",
    "https://pt.wikipedia.org/wiki/1984_(livro)",
    "https://pt.wikipedia.org/wiki/Dom_Casmurro",
    "https://pt.wikipedia.org/wiki/Cem_anos_de_solidão",
    "https://pt.wikipedia.org/wiki/O_Hobbit",
    "https://pt.wikipedia.org/wiki/Ensaio_sobre_a_Cegueira",
    "https://pt.wikipedia.org/wiki/A_Revolução_dos_Bichos",
    "https://pt.wikipedia.org/wiki/Memórias_Póstumas_de_Brás_Cubas",
]

if __name__ == "__main__":
    print("Iniciando scraping de livros da Wikipedia para PyBooks...")
    for url in URLS:
        print(f"Raspando: {url}")
        scrape_book(url)
    print("Scraping concluído! Verifique tp5/scraped_books.log")