from datetime import datetime

def add_books(books, title, description, genre, status="to_read"):
    book_id = len(books) + 1
    book = {
        "id": book_id,
        "title": title,
        "description": description,
        "genre": genre,
        "status": status,
        "added_at": datetime.now().strftime("%Y-%m-%d")
    }
    books.append(book)
    print(f"Livro '{title}' adicionado com sucesso no ID {book_id} ")
    

def list_books(books):
    if not books:
        print("Nenhum livro encontrado")
        return
    
    print("\n Livros:")
    for book in books:
        print(f"""
              ID: {book['id']} , Título: {book["title"]}
              {book["description"]}
              {book["genre"]}
              """)


def mark_book_read(books, book_id):
    for book in books:
        if book["id"] == book_id:
            book["status"] = "read"
            print(f"Book ID {book_id} marked as read.")
            return True
    print(f"Book ID {book_id} not found.")
    return False
    
def remove_books(books, book_id):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(i)
            print(f"Book ID {book_id} removido.")
            return True
    print(f"ID do Livro {book_id} não encontrado.")
    return False

