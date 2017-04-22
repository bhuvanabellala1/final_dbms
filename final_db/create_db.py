import sqlite3 as lite
import sys

con = lite.connect("store.db")

with con:
    cur = con.cursor()
    exec_curr = "CREATE TABLE Producer" +
                "(producer_id INTEGER PRIMARY KEY, email TEXT, first_name TEXT," +
                " last_name TEXT, rating REAL, phone_no INTEGER)"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Produce" +
                "(produce_id INTEGER PRIMARY KEY, producer_id INTEGER, name TEXT," +
                " harvest_date TEXT, price REAL, quantity REAL," +
                "FOREIGN KEY (producer_id) REFERENCES Producer(producer_id))"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Producer_Location" +
                "(location_id INTEGER PRIMARY KEY, producer_id INTEGER, street TEXT," +
                " unit TEXT, zipcode TEXT, city TEXT, state TEXT" +
                "FOREIGN KEY (producer_id) REFERENCES Producer(producer_id))"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Customer" +
                "(customer_id INTEGER PRIMARY KEY, email TEXT, first_name TEXT," +
                " last_name TEXT, rating REAL, phone_no INTEGER)"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Customer_Location" +
                "(location_id INTEGER PRIMARY KEY, customer_id INTEGER, street TEXT," +
                " unit TEXT, zipcode TEXT, city TEXT, state TEXT" +
                "FOREIGN KEY (customer_id) REFERENCES Customer(customer_id))"
    cur.execute(exec_curr)

    exec_curr = "CREATE TABLE Transaction" +
                "(producer_id INTEGER, customer_id INTEGER, produce_id INTEGER," +
                " date TEXT, quantity REAL," +
                "FOREIGN KEY (producer_id) REFERENCES Produce(producer_id), " +
                "FOREIGN KEY (customer_id) REFERENCES Customer(customer_id), " +\
                "FOREIGN KEY (produce_id) REFERENCES Produce(produce_id))"
    cur.execute(exec_curr)
