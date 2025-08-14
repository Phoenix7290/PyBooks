from core.core import add_books, list_books, mark_book_read, remove_books

def main():
    books = []
    while True:
        print(
            """
            PyBooks
            
            Um Indexador de Livros para salvar, listar, tipificar e excluir.
            
            1. Adicionar Livros.
            2. Listar Livros.
            3. Marcar Livros como lido.
            4. Remover Livros.
            5. Sair do Programa
            
            """
        )
        
        choice = input("Qual sua Escolha (1-5): ")
        
        if choice == "1":
            title = input("Qual o Título?")
            description = input("Descrição do livro")
            genre = input ("Qual o Genero principal?")
            
            add_books(books, title, description, genre)
        elif choice == "2":
            list_books(books)
        elif choice == "3":
            try:
                book_id = int(input("Enter book ID to mark as read: "))
                mark_book_read(books, book_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "4":
            try:
                book_id = int(input("Coloque o ID para remover:"))
                remove_books(books, book_id)
            except ValueError:
                print("ID inválido. Coloque um número.")
        elif choice == "5":
            print("Existing...")
            break
        else:
            print("Escolha Inválida. Tente Novamente.")

if __name__ == "__main__":
    main()    
