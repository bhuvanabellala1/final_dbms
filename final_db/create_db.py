import sqlite3 as lite
import sys

con = lite.connect("store.db")

with con:
    cur = con.cursor()
    exec_curr = "CREATE TABLE Producer (producer_id TEXT PRIMARY KEY, password TEXT, email TEXT, first_name TEXT, last_name TEXT, rating REAL, phone_no INTEGER, sum_ratings REAL, total_ratings INTEGER)"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Produce (produce_id INTEGER PRIMARY KEY AUTOINCREMENT, producer_id TEXT, name TEXT, harvest_date TEXT, price REAL, quantity REAL, city TEXT, FOREIGN KEY (producer_id) REFERENCES Producer(producer_id))"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Producer_Location (location_id INTEGER PRIMARY KEY, producer_id TEXT, street TEXT, unit TEXT, zipcode TEXT, city TEXT, state TEXT , FOREIGN KEY (producer_id) REFERENCES Producer(producer_id))"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Customer (customer_id TEXT PRIMARY KEY, password TEXT, email TEXT, first_name TEXT,last_name TEXT, rating REAL, phone_no INTEGER)"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Customer_Location (location_id INTEGER PRIMARY KEY, customer_id INTEGER, street TEXT, unit TEXT, zipcode TEXT, city TEXT, state TEXT , FOREIGN KEY (customer_id) REFERENCES Customer(customer_id))"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Rating (rating_id INTEGER PRIMARY KEY, customer_id INTEGER, producer_id INTEGER,  rating REAL, FOREIGN KEY (customer_id) REFERENCES Customer(customer_id), FOREIGN KEY (producer_id) REFERENCES Producer(producer_id))"
    cur.execute(exec_curr)

    # exec_curr = "CREATE TABLE Transaction (producer_id INTEGER, customer_id INTEGER, produce_id INTEGER, transdate TEXT, quantity REAL,FOREIGN KEY (producer_id) REFERENCES Produce(producer_id), FOREIGN KEY (customer_id) REFERENCES Customer(customer_id), FOREIGN KEY (produce_id) REFERENCES Produce(produce_id))"
    # cur.execute(exec_curr)
