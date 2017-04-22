import sqlite3 as lite
import sys

con = lite.connect("books.db")

with con:
	cur = con.cursor()

	cur.execute("CREATE TABLE Books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)")
	cur.execute("INSERT INTO Books (title, author) VALUES ('Web Arch', 'Kay')")
	cur.execute("INSERT INTO Books (title, author) VALUES ('Info Org', 'Bob')")
	cur.execute("INSERT INTO Books (title, author) VALUES ('Info Law', 'Deidre')")
	cur.execute("INSERT INTO Books (title, author) VALUES ('Math', 'Julie')")
