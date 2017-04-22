from flask import Flask, render_template, request, redirect
app = Flask(__name__)

import sqlite3 as lite
import sys
 
@app.route("/")
def view_all_books():
	
	con = lite.connect("books.db")
	cur = con.cursor()
	cur.execute("select id, title, author from books")
	rows = cur.fetchall()

	return render_template("index.html", **locals())

@app.route("/addbook", methods=["GET", "POST"])
def add_book():

	if request.method == "GET":
		return render_template("addbook.html", **locals())

	else:
		title = request.form["title"]
		author = request.form["author"]

		con = lite.connect("books.db")
		with con:
			cur = con.cursor()
			cur.execute("insert into Books (title, author) values ('{}', '{}')".format(title, author))

		return redirect("/")


@app.route("/book/<int:id>")
def get_book(id):

	con = lite.connect("books.db")
	cur = con.cursor()
	cur.execute("select id, title, author from books where id = " + str(id))
	rows = cur.fetchall()

	return render_template("viewbook.html", **locals())

if __name__ == "__main__":
    app.run()