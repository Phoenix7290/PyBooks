import json
from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, Text, DateTime, MetaData
from sqlalchemy.dialects.postgresql import insert as pg_insert

engine = create_engine("postgresql+psycopg2://postgres@localhost/pybooks_db", echo=False)

metadata = MetaData()

books = Table(
    "books", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255), nullable=False),
    Column("description", Text),
    Column("genre", String(100)),
    Column("status", String(50), default="to_read"),
    Column("added_at", DateTime),
    Column("user_id", Integer, nullable=False)
)

def massive_upsert_books():
    with open("data/massive_load_books.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with engine.begin() as conn:
        for item in data:
            values = {
                "title": item["title"],
                "description": item.get("description", ""),
                "genre": item.get("genre", "Fiction"),
                "status": item.get("status", "to_read"),
                "added_at": item.get("added_at") or datetime.now().isoformat(),
                "user_id": item["user_id"]
            }

            if "id" in item and item["id"] is not None:
                stmt = pg_insert(books).values(**values, id=item["id"])
                stmt = stmt.on_conflict_do_update(
                    index_elements=["id"],
                    set_=values
                ).returning(books.c.id, books.c.title)
            else:
                stmt = pg_insert(books).values(**values).returning(books.c.id, books.c.title)

            result = conn.execute(stmt)
            row = result.fetchone()
            print(f"ID {row.id} → {row.title} ({'UPDATE' if 'id' in item else 'INSERT'})")

    print("\nUPSERT concluído com sucesso!")

if __name__ == "__main__":
    massive_upsert_books()