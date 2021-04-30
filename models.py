#from . import db
from mybasic import db

class customer(db.Model) :
    customer_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(40))
    DOB = db.Column(db.String(10))
    email_id = db.Column(db.String(20))
    mob_number = db.Column(db.Integer)
    address = db.Column(db.String(100))
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

class admin(db.Model) :
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(40))
    mob_number = db.Column(db.Integer)
    a_username = db.Column(db.String(20))
    a_password = db.Column(db.String(20))

class book(db.Model) :
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50))
    author_name = db.Column(db.String(40))
    stock = db.Column(db.Integer)
    catagory = db.Column(db.String(20))
    duration_in_days = db.Column(db.Integer)
    rent_amount = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    price = db.Column(db.Integer)

class payment(db.Model) :
    transaction_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    mode = db.Column(db.String(40))
    price = db.Column(db.Integer)
    book_for = db.Column(db.String(10))
    delivery = db.Column(db.String(10))