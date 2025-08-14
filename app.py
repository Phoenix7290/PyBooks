from flask import Flask, request, render_template
from core.core import add_books, list_books, mark_book_read, remove_books, load_books

app = Flask(__name__)
books = load_books() 

@app.route('/')
def index():
    """
    Render the main page with the book management interface.
    
    Returns:
        Rendered HTML template with books list and optional message.
    """
    return render_template('index.html', books=list_books(books), message=None)

@app.route('/add', methods=['POST'])
def add():
    """
    Add a new book via form submission.
    
    Returns:
        Rendered HTML template with updated books list and success/error message.
    """
    title = request.form.get('title')
    description = request.form.get('description')
    genre = request.form.get('genre')
    success, message = add_books(books, title, description, genre)
    return render_template('index.html', books=list_books(books), message=message, error=not success)

@app.route('/mark_read/<int:book_id>')
def mark_read(book_id):
    """
    Mark a book as read by its ID.
    
    Args:
        book_id (int): The ID of the book to mark as read.
    
    Returns:
        Rendered HTML template with updated books list and message.
    """
    success, message = mark_book_read(books, book_id)
    return render_template('index.html', books=list_books(books), message=message, error=not success)

@app.route('/remove/<int:book_id>')
def remove(book_id):
    """
    Remove a book by its ID.
    
    Args:
        book_id (int): The ID of the book to remove.
    
    Returns:
        Rendered HTML template with updated books list and message.
    """
    success, message = remove_books(books, book_id)
    return render_template('index.html', books=list_books(books), message=message, error=not success)

if __name__ == '__main__':
    app.run(debug=True)