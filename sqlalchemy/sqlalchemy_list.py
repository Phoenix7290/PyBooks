from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql+psycopg2://postgres:SUASENHA@localhost/pybooks_db"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def run_query_list(sql: str):
    with Session() as sess:
        result = sess.execute(text(sql))
        return [row for row in result.fetchall()]

if __name__ == "__main__":
    queries = {
        "INNER JOIN": open("queries_postgres.sql").read().split(";")[0].strip() + ";",
        "LEFT JOIN":  open("queries_postgres.sql").read().split(";")[2].strip() + ";",
        "RIGHT JOIN": open("queries_postgres.sql").read().split(";")[4].strip() + ";"
    }

    for name, sql in queries.items():
        print(f"\n=== {name} (lista) ===")
        data = run_query_list(sql)
        for row in data:
            print(row)