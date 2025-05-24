import sqlite3
import random

def generate_isbn13():
    prefix = random.choice(["978", "979"])
    body = "".join(str(random.randint(0, 9)) for _ in range(9))
    partial_isbn = prefix + body
    check_digit = calculate_check_digit(partial_isbn)
    return partial_isbn + str(check_digit)

def calculate_check_digit(isbn):
    total = 0
    for i, digit in enumerate(isbn):
        total += int(digit) * (1 if i % 2 == 0 else 3)
    check_digit = (10 - (total % 10)) % 10
    return check_digit


conn = sqlite3.connect("library.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    writer TEXT,
    isbn INTEGER UNIQUE,
    status INTEGER
)
""")

c.execute("""CREATE TABLE IF NOT EXISTS member (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    name TEXT
    admin INTEGER)""")

def add_book(name:str, title:str, writer:str, status:str):
    if name == None or title == None or writer == None or status ==None:
        raise ValueError("Some Input is None")
    if status.lower() == "y":
        status = 1
    else:
        status = 0

    ISBN = generate_isbn13()

    c.execute("INSERT INTO book (title, writer, isbn, status) VALUES (?, ?, ?, ?)",
              (name, title, writer, ISBN, status))
    return f"Add {title} Success"


conn.close()
