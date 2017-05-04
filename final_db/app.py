from flask import Flask, render_template, request, redirect, session, escape, url_for
app = Flask(__name__)

import sqlite3 as lite
import sys
import os
app.secret_key = os.urandom(24)

@app.route("/", methods=['GET', 'POST'])
def index():
	# return render_template('index.html')
	if 'username' in session:
		print("Logged in - rendering index_1")
		return render_template('index_1.html', username=session['username'], isProducer=session['isProducer'])
	else:
		print("logging")
		return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		username = request.form.get("username")
		password = request.form.get("password")
		con = lite.connect("store.db")
		cur = con.cursor()
		cur.execute("select * from Producer where producer_id='" + username+ "';")
		producers = cur.fetchall()
		if(len(producers) == 0):
			cur.execute("select * from Customer where customer_id='" + username+ "';")
			consumers = cur.fetchall()
			if(len(consumers) == 0):
				return render_template('login.html', isValid=False)
			else:
				print("logging consumer")
				session['username'] = request.form.get("username")
				session['isProducer'] = False
				return redirect(url_for('index'))
		else:
			if(producers[0][1] == password):
				print("logging producer")
				session['username'] = request.form.get("username")
				session['isProducer'] = True
				return redirect(url_for('index'))
			else:
				return render_template('login.html', isValid=False)
	else:
		return render_template('login.html', isValid=True)

@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method=='POST':
		con = lite.connect("store.db")
		cur = con.cursor()
		cur.execute("select * from Producer where producer_id='" +request.form.get("username")+ "';")
		producers = cur.fetchall()
		cur.execute("select * from Customer where customer_id='" +request.form.get("username")+ "';")
		consumers = cur.fetchall()
		if(len(producers) == 0 and len(consumers) == 0):
			print("registering user")
			session['username'] = request.form.get("username")
			with con:
				cur = con.cursor()
				if(request.form['optradio']=="Producer"):
					print("registering user")
					session['isProducer'] = True
					cur.execute('insert into Producer(producer_id, password, email, first_name, last_name, rating, phone_no, sum_ratings, total_ratings) values ("{0}","{1}","{2}","{3}","{4}","{5}", "{6}", "{7}","{8}")'.format(request.form.get("username"),request.form.get("password"),request.form.get("email"),request.form.get("firstname"),request.form.get("lastname"),0,request.form.get("phone_no"),0,0))
				else:
					print("registering customer")
					session['isProducer'] = False
					cur.execute('insert into Customer(customer_id, password, email, first_name, last_name, phone_no) values ("{0}","{1}","{2}","{3}","{4}","{5}")'.format(request.form.get("username"),request.form.get("password"),request.form.get("email"),request.form.get("firstname"),request.form.get("lastname"),request.form.get("phone_no")))
		else:
			return render_template('register.html', isValid=False)
		return redirect(url_for('index'))
	return render_template('register.html', isValid=True)


@app.route("/add_harvest", methods=['GET', 'POST'])
def add_harvest():
	if request.method=='POST':
		con = lite.connect("store.db")
		with con:
			cur = con.cursor()
			cur.execute('insert into Produce(producer_id,name,harvest_date,price,quantity,city) values ("{0}","{1}","{2}","{3}","{4}","{5}")'.format(session['username'],request.form.get("crop_name"),request.form.get("harvest_date"),request.form.get("harvest_price"),request.form.get("harvest_quantity"),request.form.get("harvest_city")))
			cur = con.cursor()
			cur.execute("select * from Producer inner join Produce on Producer.producer_id = Produce.producer_id where Producer.producer_id='" + session['username'] + "';")
			rows = cur.fetchall()
			print(rows)
			return render_template("user_history_view.html", **locals())
	else:
		return render_template('add_harvest.html')

@app.route("/user_history_view")
def user_history_view():
	con = lite.connect("store.db")
	cur = con.cursor()
	cur.execute("select * from Producer inner join Produce on Producer.producer_id = Produce.producer_id where Producer.producer_id='" + session['username'] + "';")
	rows = cur.fetchall()
	return render_template("user_history_view.html", **locals())

@app.route("/find", methods=['GET', 'POST'])
def find_produce():
	print("FINDING PRODUCE")
	print(request.form.get("city"))
	city=request.form.get("city")
	con = lite.connect("store.db")
	cur = con.cursor()
	cur.execute("select Producer.first_name, Producer.last_name, Producer.email, Produce.name, Produce.harvest_date , Produce.price , Produce.quantity from Produce inner join Producer on Produce.producer_id = Producer.producer_id where Produce.city = '" + request.form.get("city") + "';")
	rows = cur.fetchall()
	print(rows)
	return render_template("find_produce.html", **locals())

@app.route("/logout")
def logout():
	print("Logging out")
	session.pop('username', None)
	session.pop('isProducer', None)
	return redirect(url_for('index'))

@app.route("/see_prices")
def see_prices():
	print("Seeing competitor prices")
	con = lite.connect("store.db")
	cur = con.cursor()
	cur.execute("select p2.name, p1.price, p2.producer_id, p2.price, p2.city from Produce p1, Produce p2 where p1.name = p2.name and p2.producer_id != p1.producer_id and p1.producer_id = '" + session['username'] + "';")
	rows = cur.fetchall()
	print(rows)
	return render_template("see_prices.html", **locals())

@app.route("/edit/<int:oid>", methods=['GET', 'POST'])
def edit(oid):
	if request.method=='POST':
		con = lite.connect("store.db")
		with con:
			cur = con.cursor()
			print("updating")
			cur.execute("update Produce set name=?,harvest_date=?,price=?,quantity=?,city=? where Produce.produce_id=?;",(request.form.get("crop_name"),request.form.get("harvest_date"),request.form.get("harvest_price"),request.form.get("harvest_quantity"),request.form.get("harvest_city"),str(oid)))
			cur = con.cursor()
			print("selecting")
			cur.execute("select * from Producer inner join Produce on Producer.producer_id = Produce.producer_id where Producer.producer_id='" + session['username'] + "';")
			rows = cur.fetchall()
			print(rows)
			return render_template("user_history_view.html", **locals())
	print("EDITING")
	con = lite.connect("store.db")
	cur = con.cursor()
	cur.execute("select * from Produce where Produce.producer_id='" + session['username'] + "' and Produce.produce_id="+str(oid)+";")
	rows = cur.fetchall()
	return render_template("edit_harvest.html", **locals())

@app.route("/rate", methods=['GET', 'POST'])
def rate():
	if request.method=='POST':
		print(request.form.get("username"))
		print(request.form.get("rating"))
		con = lite.connect("store.db")
		cur = con.cursor()
		cur.execute("select * from Producer where Producer.producer_id='"+request.form.get("username")+"';")
		counts = cur.fetchall()
		if(len(counts) > 0):
			cur.execute("select * from Rating where Rating.customer_id='" + session['username'] + "' and Rating.producer_id='"+request.form.get("username")+"';")
			rows = cur.fetchall()
			print(rows)
			prev_rating = 0
			if(len(rows)==0):
				with con:
					print("inserting new rating")
					cur = con.cursor()
					cur.execute('insert into Rating(customer_id,producer_id,rating) values ("{0}","{1}","{2}")'.format(session['username'],request.form.get("username"),int(request.form.get("rating"))))
					print("Updating Producer rating")
					cur.execute("update Producer set sum_ratings=?,total_ratings=? where Producer.producer_id=?;",(counts[0][7] + int(request.form.get("rating")), counts[0][8]+1, request.form.get("username")))
			else:
				with con:
					print("updating rating")
					prev_rating = int(rows[0][3])
					cur = con.cursor()
					print("updating ratings table")
					cur.execute("update Rating set rating=? where Rating.producer_id=? and Rating.customer_id=?;",(int(request.form.get("rating")),request.form.get("username"),session['username']))
					print("updating producers table")
					cur.execute("update Producer set sum_ratings=? where Producer.producer_id=?;",(counts[0][7] + int(request.form.get("rating")) - prev_rating, request.form.get("username")))
			print("Rating")
			cur.execute("select Rating.producer_id, Rating.rating, Producer.sum_ratings/Producer.total_ratings from Rating inner join Producer on Rating.producer_id=Producer.producer_id where Rating.customer_id='" + session['username'] + "';")
			rows = cur.fetchall()
			print(rows)
			return render_template("rate.html", **locals())
		else:
			return redirect(url_for('index'))

	con = lite.connect("store.db")
	cur = con.cursor()
	print("Rating")
	cur.execute("select Rating.producer_id, Rating.rating, Producer.sum_ratings/Producer.total_ratings from Rating inner join Producer on Rating.producer_id=Producer.producer_id where Rating.customer_id='" + session['username'] + "';")
	rows = cur.fetchall()
	print(rows)
	return render_template("rate.html", **locals())

if __name__ == "__main__":
    app.run()
