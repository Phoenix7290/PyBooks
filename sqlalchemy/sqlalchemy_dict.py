from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Config
DB_URL = "postgresql+psycopg2://postgres@localhost/pybooks_db"
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)


def run_query_dict(sql: str):
    with Session() as sess:
        result = sess.execute(text(sql))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]

if __name__ == "__main__":
    queries = {
        "INNER JOIN": open("queries_join.sql").read().split(";")[0].strip() + ";",
        "LEFT JOIN":  open("queries_join.sql").read().split(";")[2].strip() + ";",
        "RIGHT JOIN": open("queries_join.sql").read().split(";")[4].strip() + ";"
    }

    for name, sql in queries.items():
        print(f"\n=== {name} ===")
        data = run_query_dict(sql)
        for d in data:
            print(d)