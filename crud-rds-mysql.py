from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# MySQL connection configuration
DB_HOST = 'mysql-container'
DB_USER = 'admin'
DB_PASSWORD = 'your_password'
DB_NAME = 'mybooks'

# Create connection to the MySQL database
db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create the 'mybook' table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS mybooks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author VARCHAR(255),
    title VARCHAR(255),
    isbn INT
)
"""
cursor.execute(create_table_query)


# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    select_query = "SELECT * FROM mybook"
    cursor.execute(select_query)
    books = cursor.fetchall()
    
    # Convert the result to a list of dictionaries
    books_list = []
    for book in books:
        book_dict = {
            'id': book[0],
            'author': book[1],
            'title': book[2],
            'isbn': book[3]
        }
        books_list.append(book_dict)
    
    return jsonify(books_list)


# Route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    book_data = request.get_json()
    author = book_data.get('author')
    title = book_data.get('title')
    isbn = book_data.get('isbn')
    
    insert_query = "INSERT INTO mybook (author, title, isbn) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (author, title, isbn))
    db.commit()
    
    return jsonify({'message': 'Book added successfully'}), 201


# Route to update an existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book_data = request.get_json()
    author = book_data.get('author')
    title = book_data.get('title')
    isbn = book_data.get('isbn')
    
    update_query = "UPDATE mybook SET author=%s, title=%s, isbn=%s WHERE id=%s"
    cursor.execute(update_query, (author, title, isbn, book_id))
    db.commit()
    
    return jsonify({'message': 'Book updated successfully'})


# Route to delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    delete_query = "DELETE FROM mybook WHERE id=%s"
    cursor.execute(delete_query, book_id)
    db.commit()
    
    return jsonify({'message': 'Book deleted successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

