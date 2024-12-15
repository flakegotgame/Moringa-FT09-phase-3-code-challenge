import sqlite3

# Database Connection Setup
DATABASE_NAME = "articles.db"

# Connect to the database
def connect():
    return sqlite3.connect(DATABASE_NAME)

# Initialize Database Tables
def initialize_database():
    connection = connect()
    cursor = connection.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE CHECK(length(name) > 0)
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS magazines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE CHECK(length(name) BETWEEN 2 AND 16),
        category TEXT NOT NULL CHECK(length(category) > 0)
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL CHECK(length(title) BETWEEN 5 AND 50),
        author_id INTEGER NOT NULL,
        magazine_id INTEGER NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors (id),
        FOREIGN KEY (magazine_id) REFERENCES magazines (id)
    );''')

    connection.commit()
    connection.close()

# Author Model
class Author:
    def __init__(self, name):
        self.name = name
        self.id = self.create_author()

    def create_author(self):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
        connection.commit()
        author_id = cursor.lastrowid
        connection.close()
        return author_id

    @staticmethod
    def get_author(author_id):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        author = cursor.fetchone()
        connection.close()
        return author

# Magazine Model
class Magazine:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.id = self.create_magazine()

    def create_magazine(self):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
        connection.commit()
        magazine_id = cursor.lastrowid
        connection.close()
        return magazine_id

    @staticmethod
    def get_magazine(magazine_id):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
        magazine = cursor.fetchone()
        connection.close()
        return magazine

# Article Model
class Article:
    def __init__(self, title, author, magazine):
        self.title = title
        self.author_id = author.id
        self.magazine_id = magazine.id
        self.id = self.create_article()

    def create_article(self):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (self.title, self.author_id, self.magazine_id),
        )
        connection.commit()
        article_id = cursor.lastrowid
        connection.close()
        return article_id

    @staticmethod
    def get_article(article_id):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        article = cursor.fetchone()
        connection.close()
        return article

# Initialize the database
if __name__ == "__main__":
    initialize_database()

    # Example usage
    author = Author("Jane Doe")
    magazine = Magazine("Tech Weekly", "Technology")
    article = Article("AI Revolution", author, magazine)

    print("Author:", Author.get_author(author.id))
    print("Magazine:", Magazine.get_magazine(magazine.id))
    print("Article:", Article.get_article(article.id))
