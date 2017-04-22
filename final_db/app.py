from flask import Flask, render_template, request, redirect, session, escape
app = Flask(__name__)

import sqlite3 as lite
import sys
import os
app.secret_key = os.urandom(24)

@app.route("/", methods=['GET', 'POST'])
def index():

	if 'username' in session:
		return render_template('home.html')
	else:
		return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		print request.form.get("username")
		print request.form.get("password")
		return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method=='POST':
		print  request.form.get("username")
		
	return render_template('register.html')



# <form action="/addbook" class="col-md-10" method="POST">
# 	<div class="form-group">
# 		<label for="title">Title:</label>
# 		<input type="text" class="form-control" id="title" name="title">
# 	</div>
# 	<div class="form-group">
# 		<label for="author">Author:</label>
# 		<input type="text" class="form-control" id="author" name="author">
# 	</div>
#
# 	<button type="submit" class="btn btn-default">Submit</button>
# </form>

if __name__ == "__main__":
    app.run()
