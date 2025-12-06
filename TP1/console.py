import mysql.connector
from datetime import datetime

# Conexão ao DB (ajuste credenciais)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="", 
        database="pybooks_db"
    )

def add_book_db(title, description, genre, status="to_read"):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO books (title, description, genre, status, added_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        added_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(query, (title, description, genre, status, added_at))
        conn.commit()
        print(f"Livro '{title}' adicionado com sucesso.")
    except Exception as e:
        print(f"Erro ao adicionar livro: {e}")
    finally:
        cursor.close()
        conn.close()

def list_books_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title, description, genre, status, added_at FROM books")
        books = cursor.fetchall()
        if not books:
            print("Nenhum livro encontrado.")
            return
        print("\nLivros:")
        for book in books:
            print(f"ID: {book[0]}, Título: {book[1]}, Descrição: {book[2]}, Gênero: {book[3]}, Status: {book[4]}, Adicionado em: {book[5]}")
    except Exception as e:
        print(f"Erro ao listar livros: {e}")
    finally:
        cursor.close()
        conn.close()

def mark_book_read_db(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE books SET status = 'read' WHERE id = %s", (book_id,))
        if cursor.rowcount == 0:
            print(f"Livro ID {book_id} não encontrado.")
            return
        conn.commit()
        print(f"Livro ID {book_id} marcado como lido.")
    except Exception as e:
        print(f"Erro ao marcar livro: {e}")
    finally:
        cursor.close()
        conn.close()

def remove_book_db(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        if cursor.rowcount == 0:
            print(f"Livro ID {book_id} não encontrado.")
            return
        conn.commit()
        print(f"Livro ID {book_id} removido.")
    except Exception as e:
        print(f"Erro ao remover livro: {e}")
    finally:
        cursor.close()
        conn.close()

# Admin
def list_users_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, username, role, department, active FROM users")
        users = cursor.fetchall()
        if not users:
            print("Nenhum usuário encontrado.")
            return
        print("\nUsuários:")
        for user in users:
            print(f"ID: {user[0]}, Nome: {user[1]}, Username: {user[2]}, Role: {user[3]}, Departamento: {user[4]}, Ativo: {user[5]}")
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
    finally:
        cursor.close()
        conn.close()

def add_user_db(name, username, password_hash, role, department):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO users (name, username, password_hash, role, department, join_date, active)
        VALUES (%s, %s, %s, %s, %s, CURDATE(), TRUE)
        """
        cursor.execute(query, (name, username, password_hash, role, department))
        conn.commit()
        print(f"Usuário '{username}' adicionado com sucesso.")
    except Exception as e:
        print(f"Erro ao adicionar usuário: {e}")
    finally:
        cursor.close()
        conn.close()

def remove_user_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        if cursor.rowcount == 0:
            print(f"Usuário ID {user_id} não encontrado.")
            return
        conn.commit()
        print(f"Usuário ID {user_id} removido.")
    except Exception as e:
        print(f"Erro ao remover usuário: {e}")
    finally:
        cursor.close()
        conn.close()

def update_user_active_db(user_id, active):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET active = %s WHERE id = %s", (active, user_id))
        if cursor.rowcount == 0:
            print(f"Usuário ID {user_id} não encontrado.")
            return
        conn.commit()
        status = "ativo" if active else "inativo"
        print(f"Usuário ID {user_id} marcado como {status}.")
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
    finally:
        cursor.close()
        conn.close()

# Admin menu
def main():
    while True:
        print("""
        PyBooks - Modo Super Admin (Terminal)
        
        1. Adicionar Livro
        2. Listar Livros
        3. Marcar Livro como Lido
        4. Remover Livro
        5. Listar Usuários
        6. Adicionar Usuário
        7. Remover Usuário
        8. Ativar/Desativar Usuário
        9. Sair
        """)
        
        choice = input("Escolha (1-9): ")
        
        if choice == "1":
            title = input("Título: ")
            description = input("Descrição: ")
            genre = input("Gênero: ")
            add_book_db(title, description, genre)
        elif choice == "2":
            list_books_db()
        elif choice == "3":
            try:
                book_id = int(input("ID do Livro para marcar como lido: "))
                mark_book_read_db(book_id)
            except ValueError:
                print("ID inválido.")
        elif choice == "4":
            try:
                book_id = int(input("ID do Livro para remover: "))
                remove_book_db(book_id)
            except ValueError:
                print("ID inválido.")
        elif choice == "5":
            list_users_db()
        elif choice == "6":
            name = input("Nome: ")
            username = input("Username: ")
            password_hash = input("Password Hash: ") 
            role = input("Role (ex: admin/user): ")
            department = input("Departamento: ")
            add_user_db(name, username, password_hash, role, department)
        elif choice == "7":
            try:
                user_id = int(input("ID do Usuário para remover: "))
                remove_user_db(user_id)
            except ValueError:
                print("ID inválido.")
        elif choice == "8":
            try:
                user_id = int(input("ID do Usuário: "))
                active = input("Ativar (1) ou Desativar (0)? ") == "1"
                update_user_active_db(user_id, active)
            except ValueError:
                print("ID inválido.")
        elif choice == "9":
            print("Saindo...")
            break
        else:
            print("Escolha inválida.")

if __name__ == "__main__":
    main()