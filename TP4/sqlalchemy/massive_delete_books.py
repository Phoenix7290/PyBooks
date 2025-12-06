import json
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, delete

engine = create_engine("postgresql+psycopg2://postgres@localhost/pybooks_db", echo=False)

metadata = MetaData()

books_table = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255)),        
    Column("user_id", Integer)         
)

def massive_delete_books():
    with open("data/massive_delete_books.json", "r", encoding="utf-8") as f:
        ids_to_delete = [item["id"] for item in json.load(f)]

    if not ids_to_delete:
        print("Nenhum ID para deletar no JSON.")
        return

    stmt = (
        delete(books_table)
        .where(books_table.c.id.in_(ids_to_delete))
        .returning(books_table.c.id, books_table.c.title)
    )
    
    with engine.begin() as conn:
        result = conn.execute(stmt)
        deleted_rows = result.fetchall()

    print(f"\n{len(deleted_rows)} livro(s) deletado(s) com sucesso:")
    for row in deleted_rows:
        print(f"   → ID {row.id} | {row.title}")

    deleted_ids = {row.id for row in deleted_rows}
    not_found = set(ids_to_delete) - deleted_ids
    if not_found:
        print(f"\nIDs não encontrados (não existiam): {sorted(not_found)}")

if __name__ == "__main__":
    massive_delete_books()