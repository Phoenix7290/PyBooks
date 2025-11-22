from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres@localhost/pybooks_db")
Session = sessionmaker(bind=engine)

with Session() as s:
    result = s.execute(text("SELECT id, title, status, genre FROM books ORDER BY id"))
    print("Livros atuais no banco:")
    for r in result:
        print(f"  {r.id:2d} | {r.title:30} | {r.status:8} | {r.genre}")