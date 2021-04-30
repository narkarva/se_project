from flask import Flask, render_template, redirect, url_for, request, flash
import requests
import flask_login
#from flask_login import login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
import os, random

#global got_book_id, y, quant, total_price

db = SQLAlchemy()
DBNAME = 'database5.db'
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SE_PROJECT_GRP_118'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DBNAME}'
    db.init_app(app)
    return app

app = create_app()
from models import *

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mylogin')
def my_login() :
    return render_template('mylogin.html')

@app.route('/mysignup')
def my_signup() :
    return render_template('mysignup.html')

@app.route('/login', methods=['POST', 'GET'])
def Login() :
    if request.method == "POST" :
        username = request.form.get('username')
        password = request.form.get('password')
        a_username = request.form.get('a_username')
        a_password = request.form.get('a_password')
        found_customer = customer.query.filter_by(username=username).first()
        found_admin = admin.query.filter_by(a_username=a_username).first()
        #print(flask_login.current_user)
        if found_customer :
            if password == found_customer.password :
                flask_login.current_user = found_customer
                return render_template('customerdashboard.html')
            else :
                flash('Wrong customer password!, try again')
                return render_template('mylogin.html')
        elif found_admin :
            if a_password == found_admin.a_password :
                flask_login.current_user = found_admin
                print("Admin logged in with id ", flask_login.current_user.admin_id)
                return render_template('admindashboard.html')
            else :
                flash('Wrong admin password!, try again')
                return render_template('mylogin.html')
        else :
            flash('Wrong username!, try again')
            return render_template('mylogin.html')

@app.route('/signup', methods=['POST', 'GET'])
def Signup() :
    if request.method == "POST" :
        seterr = 0
        full_name = request.form.get('full_name')
        ful = full_name.split()
        ful = "".join(ful)
        if ful.isalpha() != True :
            seterr = 1
            flash('Your full name can only contain alphabets! Please enter valid name')
        DOB = request.form.get('DOB')
        email_id = request.form.get('email_id')
        if '@' not in email_id :
            seterr = 1
            flash('Email ID is invalid! Please enter valid email ID')
        mob_number = request.form.get('mob_number')
        if len(mob_number) != 10 or mob_number.isdigit() != True :
            seterr = 1
            flash('Mobile number should be 10 digit number! Enter valid mobile number')
        address = request.form.get('address')
        username = request.form.get('username')
        password = request.form.get('password')
        if seterr == 1 :
            flash('Please enter valid information at specified fields')
            return render_template('mysignup.html')
        confpassword = request.form.get('confpassword')
        if password == confpassword :
            alexists = customer.query.filter_by(username=username).first()
            if alexists == None :
                new_customer = customer(full_name=full_name, DOB=DOB, email_id=email_id, mob_number=int(mob_number), address=address, username=username, password=password)
                db.session.add(new_customer)
                db.session.commit()
                return render_template('mylogin.html')
            else :
                flash('Your set up username already exists!, please try some other username')
                return render_template('mysignup.html')
        else :
            flash('Your confirmed password doesnt match the original!')
            return render_template('mysignup.html')

@app.route('/admsignup')
def adm_signup() :
    return render_template('adminsignup.html')

@app.route('/adminsignup', methods=['POST', 'GET'])
def admin_signup() :
    if request.method == "POST" :
        admin_name = request.form.get('admin_name')
        amob_number = request.form.get('mob_number')
        if len(amob_number) != 10 or amob_number.isdigit() != True :
            flash('Mobile number is invalid')
            return render_template('adminsignup.html')
        a_username = request.form.get('a_username')
        a_password = request.form.get('a_password')
        a_confpassword = request.form.get('a_confpassword')
        if a_password == a_confpassword :
            new_admin = admin(admin_name=admin_name, mob_number=int(amob_number), a_username=a_username, a_password=a_password)
            db.session.add(new_admin)
            db.session.commit()
            return render_template('mylogin.html')
        else :
            flash('Your confirmed password and current password doesnt match!')
            return render_template('adminsignup.html')

@app.route('/viewbooks', methods=['POST', 'GET'])
def view() :
    return render_template('view.html', entries=book.query.filter_by().all())

@app.route('/viewback', methods=['POST', 'GET'])
def view_back() :
    if request.method == "POST" :
        if request.form['submit'] == "Back" :
            return render_template('customerdashboard.html')

@app.route('/handprofile', methods=['POST', 'GET'])
def hand_profile() :
    myuser = flask_login.current_user
    return render_template('profile.html', userinfo=myuser)

@app.route('/handhistory', methods=['POST', 'GET'])
def hand_history() :
        ent = payment.query.filter_by(customer_id=flask_login.current_user.customer_id).all()
        total_items = []
        for a in ent :
            item_list = []
            item_list.append(a.transaction_id)
            item_list.append(a.price)
            item_list.append(a.quantity)
            item_list.append(a.book_for)
            bdetail = book.query.filter_by(book_id=a.book_id).first()
            item_list.append(bdetail.book_name)
            item_list.append(bdetail.author_name)
            item_list.append(a.delivery)
            total_items.append(item_list)

        return render_template('customerhistory.html', values=total_items)
        
@app.route('/handhistory_back', methods=['POST', 'GET'])
def hand_history_back() :
    if request.method == "POST" :
        if request.form['submit'] == "Back" :
            return render_template('customerdashboard.html')

@app.route('/a_seeall', methods=['POST', 'GET'])
def see_all() :
        ent = payment.query.filter_by().all()
        total_items = []
        for a in ent :
            item_list = []
            item_list.append(a.transaction_id)
            item_list.append(a.price)
            item_list.append(a.quantity)
            item_list.append(a.book_for)
            bdetail = book.query.filter_by(book_id=a.book_id).first()
            item_list.append(bdetail.book_name)
            item_list.append(bdetail.author_name)
            item_list.append(a.customer_id)
            item_list.append(bdetail.book_id)
            item_list.append(a.delivery)
            total_items.append(item_list)

        return render_template('seeall_t.html', values=total_items)
        
@app.route('/seeall_back', methods=['POST', 'GET'])
def seeall_back() :
    if request.method == "POST" :
        if request.form['submit'] == "Back" :
            return render_template('admindashboard.html')

@app.route('/handbrent', methods=['POST', 'GET'])
def hand_brent() :
    #d_flag = 0
    return render_template('rentfilter.html')

@app.route("/rentsearch", methods=["POST", "GET"])
def myrentsearch() :
    if request.method == "POST":
        if request.form['submit'] == "submit" :
            book_name = request.form.get("book_name")
            author_name = request.form.get("author_name")
            catagory = request.form.get("catagory")
            book_name = book_name.lower()
            author_name = author_name.lower()
            catagory = catagory.lower()
            if book_name and author_name and catagory:
                filtered_values = book.query.filter_by(book_name=book_name, author_name=author_name, catagory=catagory).all()
            elif book_name and author_name and (not catagory):
                filtered_values = book.query.filter_by(book_name=book_name, author_name=author_name).all()	
            elif book_name and catagory and (not author_name):
                filtered_values = book.query.filter_by(book_name=book_name, catagory=catagory).all()
            elif catagory and (not book_name) and (not author_name):
                filtered_values = book.query.filter_by(catagory=catagory).all()
            elif author_name and catagory and (not book_name):
                filtered_values = book.query.filter_by(author_name=author_name, catagory=catagory).all()
            elif author_name and (not book_name) and (not catagory):
                filtered_values = book.query.filter_by(author_name=author_name).all()
            elif book_name and (not author_name) and (not catagory):
                filtered_values = book.query.filter_by(book_name=book_name).all()
            else : 
                flash('Enter atleast one field to search from!!')
                flash('If you have entered a field, then there are no matching results')
                return render_template('rentfilter.html')
            
            for x in filtered_values :
                if (not x.rent_amount) or (not x.duration_in_days) :
                    filtered_values.remove(x)
            flash('Following are the search results for your search')
            global d_flag
            d_flag = 0
            return render_template("display.html", values=filtered_values, d_flag=d_flag)
        elif request.form['submit'] == "Back" :
            return render_template('customerdashboard.html')

@app.route('/handbpurchase', methods=['POST', 'GET'])
def hand_bpurchase() :
    #d_flag = 1
    return render_template('purchasefilter.html')

@app.route("/purchasesearch", methods=["POST", "GET"])
def mypurchasesearch() :
    if request.method == "POST":
        if request.form['submit'] == "submit" :
            book_name = request.form.get("book_name")
            author_name = request.form.get("author_name")
            catagory = request.form.get("catagory")
            book_name = book_name.lower()
            author_name = author_name.lower()
            catagory = catagory.lower()
            if book_name and author_name and catagory:
                filtered_values = book.query.filter_by(book_name=book_name, author_name=author_name, catagory=catagory).all()
            elif book_name and author_name and (not catagory):
                filtered_values = book.query.filter_by(book_name=book_name, author_name=author_name).all()	
            elif book_name and catagory and (not author_name):
                filtered_values = book.query.filter_by(book_name=book_name, catagory=catagory).all()
            elif catagory and (not book_name) and (not author_name):
                filtered_values = book.query.filter_by(catagory=catagory).all()
            elif author_name and catagory and (not book_name):
                filtered_values = book.query.filter_by(author_name=author_name, catagory=catagory).all()
            elif author_name and (not book_name) and (not catagory):
                filtered_values = book.query.filter_by(author_name=author_name).all()
            elif book_name and (not author_name) and (not catagory):
                filtered_values = book.query.filter_by(book_name=book_name).all()
            else : 
                flash('Enter atleast one field to search from!!')
                return render_template('rentfilter.html')
            
            for x in filtered_values :
                if (not x.price) or (not x.book_type) :
                    filtered_values.remove(x)
            flash('Following are the search results for your search')
            global d_flag
            d_flag = 1
            return render_template("display.html", values=filtered_values, d_flag=d_flag)
        elif request.form['submit'] == "Back" :
            return render_template('customerdashboard.html')

#@app.route('/viewbooks', methods=['POST', 'GET'])
#def view_books() :
#    pass

@app.route('/cngpassword', methods=['POST', 'GET'])
def cng_password() :
    if request.method == "POST" :
        if request.form.get('proceed') == "Change Password" :
            oldpassword = request.form.get('oldpassword')
            newpassword = request.form.get('newpassword')
            confnewpass = request.form.get('confnewpass')
            if newpassword :
                if oldpassword == flask_login.current_user.password :
                    if newpassword == confnewpass :
                        updateuser = flask_login.current_user
                        num_rows_updated = customer.query.filter_by(customer_id=updateuser.customer_id).update(dict(password=newpassword))
                        print(num_rows_updated)
                        #flask_login.current_user.password = newpassword
                        #db.session.add(flask_login.current_user)
                        db.session.commit()
                        flask_login.current_user = customer.query.filter_by(customer_id=updateuser.customer_id).first()
                        flash('Password Changed successfully!')
                        return render_template('customerdashboard.html')
                    else :
                        flash('Please correctly confirm your password!')
                        return render_template('profile.html', userinfo=flask_login.current_user)
                else :
                    flash("Entered old password doesn't match! Enter correct old password")
                    return render_template('profile.html', userinfo=flask_login.current_user)
            else :
                flash('Fill the new password field correctly!')
                return render_template('profile.html', userinfo=flask_login.current_user)
        elif request.form.get('proceed') == "Back" :
            return render_template('customerdashboard.html')

@app.route('/a_handprofile', methods=['POST', 'GET'])
def a_hand_profile() :
    myuser = flask_login.current_user
    return render_template('adminprofile.html', userinfo=myuser)

@app.route('/a_cngpassword', methods=['POST', 'GET'])
def a_cng_password() :
    if request.method == "POST" :
        if request.form.get('proceed') == "Change Password" :
            oldpassword = request.form.get('oldpassword')
            newpassword = request.form.get('newpassword')
            confnewpass = request.form.get('confnewpass')
            if newpassword :
                if oldpassword == flask_login.current_user.a_password :
                    if newpassword == confnewpass :
                        updateuser = flask_login.current_user
                        num_rows_updated = admin.query.filter_by(admin_id=updateuser.admin_id).update(dict(a_password=newpassword))
                        #print(num_rows_updated)
                        db.session.commit()
                        flask_login.current_user = admin.query.filter_by(admin_id=updateuser.admin_id).first()
                        flash('Password Changed successfully!')
                        return render_template('admindashboard.html')
                    else :
                        flash('Please correctly confirm your password!')
                        return render_template('adminprofile.html', userinfo=flask_login.current_user)
                else :
                    flash("Entered old password doesn't match! Enter correct old password")
                    return render_template('adminprofile.html', userinfo=flask_login.current_user)
            else :
                flash('Fill the new password field correctly!')
                return render_template('adminprofile.html', userinfo=flask_login.current_user)
        elif request.form.get('proceed') == "Back" :
            return render_template('admindashboard.html')

@app.route('/a_handbooks', methods=['POST', 'GET'])
def book_page() :
    return render_template('book.html')

@app.route('/a_hand_book', methods=['POST', 'GET'])
def a_hand_books() :
    if request.method == "POST":
        if request.form['submit'] == "Submit" :
            book_name = request.form.get("book_name")
            book_name = book_name.lower()
            author_name = request.form.get("author_name")
            author_name = author_name.lower()
            aut = author_name.split()
            aut = "".join(aut)
            if aut.isalpha() != True :
                flash('Author name cannot have numbers!')
                return render_template('book.html')
            stock = request.form.get("stock")
            catagory = request.form.get("catagory")
            catagory = catagory.lower()
            duration_in_days = request.form.get("duration_in_days")
            rent_amount = request.form.get("rent_amount")
            if  rent_amount != "" and rent_amount.isdigit() != True :
                flash('Invalid rent amount entered')
                return render_template('book.html')
            book_type = request.form.get("book_type")
            price = request.form["price"]
            if price != "" and price.isdigit() != True :
                flash('You entered non integer value for price')
                return render_template('book.html')
            print(type(price))
            print(type(rent_amount))
            found_book = book.query.filter_by(book_name=book_name).first()
            if found_book == None :
                #First case handles only books for purchase.
                #Second case handles books for rent or both.
                #Rest cases are error cases.
                if duration_in_days == "" and stock.isdigit() == True :
                    new_book = book(book_name=book_name, author_name=author_name, stock=int(stock), catagory=catagory, duration_in_days=duration_in_days, rent_amount=rent_amount, book_type=book_type, price=int(price))
                    db.session.add(new_book)
                    db.session.commit()
                elif (stock.isdigit() == True) and (duration_in_days.isdigit() == True) and int(stock) > 0 and int(duration_in_days) >= 1 :
                    new_book = book(book_name=book_name, author_name=author_name, stock=int(stock), catagory=catagory, duration_in_days=int(duration_in_days), rent_amount=int(rent_amount), book_type=book_type, price=price)
                    db.session.add(new_book)
                    db.session.commit()
                elif (stock.isdigit() == True) and int(stock) <= 0 :
                    flash('Stock cannot be negative! Enter valid value for stock of books')
                elif stock.isdigit() == False :
                    flash('Stock has to be positive integer!')
                else : 
                    flash('Duration in days is entered invalid! Enter valid rent duration')
                return render_template('book.html')
            else :
                if (stock.isdigit() == True) and int(stock) > 0 :
                    num_rows_updated = book.query.filter_by(book_id=found_book.book_id).update(dict(stock=int(stock)+found_book.stock))
                    db.session.commit()
                    flash("book already exists! Updated it's stock")
                else :
                    flash('Stock entered is invalid! Enter valid value for stock of books')
                return render_template('book.html')
        elif request.form['submit'] == "Back" :
            return render_template('admindashboard.html')

@app.route("/getbook", methods=["POST", "GET"])
def Get_book():
    global got_book_id, y, total_price, quant
    if request.method == "POST":
        got_book_id = request.form.get("select_book")
        print(got_book_id)
        
        
        try :
            quant = int(request.form.get(str(got_book_id)))
            print(type(quant))
            print(quant)
            total_price = quant * int(book.query.filter_by(book_id=int(got_book_id)).first().price)
        except :
            quant = 1
            total_price =  int(book.query.filter_by(book_id=int(got_book_id)).first().rent_amount)
		#print(type(book_id))
        y = random.randint(1, 10000)
        
        return render_template("payment.html", values=book.query.filter_by(book_id=int(got_book_id)).all(), random_num=y, total_price=total_price)

@app.route('/dopayment', methods=['POST', 'GET'])
def do_payment() :
    if request.method == "POST" :
        #CC = 2
        U_list = None
        C_list = None
        book_for = ""
        if d_flag == 0 :
            book_for = "rent"
        else :
            book_for = "purchase"

        mymode = request.form.get('mode')
        delivery = request.form.get('delivery')
        if delivery == "Delivery":
            delivery = "yes"
        else:
            delivery = "no"
        if (request.form.get('OTP')) == "" :
            flash('CAPTCHA not verified!')
            return render_template("payment.html", values=book.query.filter_by(book_id=int(got_book_id)).all(), random_num=y, total_price=total_price)

        if y == int(request.form.get('OTP')) :
            if mymode == "UPI" :
                CC = 2
                U_list = []
                p_mobile_num = request.form.get('UPInm')
                if len(p_mobile_num) != 10 or p_mobile_num.isdigit() != True :
                    flash('Entered mobile number is invalid!')
                    return render_template("payment.html", values=book.query.filter_by(book_id=int(got_book_id)).all(), random_num=y, total_price=total_price)
                p_user_nm = request.form.get('UPIname')
                if p_mobile_num :
                    if int(p_mobile_num) != flask_login.current_user.mob_number :
                        flash('Your UPI mobile number doesnt match! Enter valid one')
                        return render_template("payment.html", values=book.query.filter_by(book_id=int(got_book_id)).all(), random_num=y, total_price=total_price)
                    else :
                        print("At right place")
                        new_payment = payment(customer_id=flask_login.current_user.customer_id, book_id=int(got_book_id), mode=mymode, quantity=quant, price=total_price, book_for=book_for, delivery=delivery) 
                        U_list.append(p_mobile_num)
                        U_list.append(p_user_nm)
                else :
                    flash('No mobile number entered. Compulsory for UPI')
                    return render_template("payment.html", values=book.query.filter_by(book_id=int(got_book_id)).all(), random_num=y, total_price=total_price)
            elif mymode == "Credit Card" or "Debit Card":
                C_list = []
                if mymode == "Credit Card" :
                    CC = 0
                else :
                    CC = 1
                p_chname = request.form.get('chname')
                p_Cnum = request.form.get('cardnum')
                if len(p_Cnum) != 12 or p_Cnum.isdigit() != True :
                    flash('Invalid card number')
                    return render_template("payment.html", values=book.query.filter_by(book_id=int(got_book_id)).all(), random_num=y, total_price=total_price)
                p_exp = request.form.get('expdate')
                p_cvv = request.form.get('cvv')
                if len(p_cvv) != 3 or p_cvv.isdigit() != True :
                    flash('Entered cvv number is invalid')
                    return render_template("payment.html", values=book.query.filter_by(book_id=int(got_book_id)).all(), random_num=y, total_price=total_price)
                if not(p_Cnum) or not(p_exp) or not(p_cvv) :
                    flash('Fill card details properly')
                    return render_template("payment.html", values=book.query.filter_by(book_id=int(got_book_id)).all(), random_num=y, total_price=total_price)
                new_payment = payment(customer_id=flask_login.current_user.customer_id, book_id=int(got_book_id), mode=mymode, quantity=quant, price=total_price, book_for=book_for, delivery=delivery)
                C_list.append(p_chname)
                C_list.append(p_Cnum)
                C_list.append(p_exp)
                C_list.append(p_cvv)
            db.session.add(new_payment)
            db.session.commit()
            mystock = book.query.filter_by(book_id=int(got_book_id)).first()
            num_rows_updated1 = book.query.filter_by(book_id=int(got_book_id)).update(dict(stock=int(mystock.stock)-quant))
            db.session.commit()
            ts = payment.query.filter_by(book_id=int(got_book_id), customer_id=flask_login.current_user.customer_id).all()
            try :
                tss = ts[len(ts)-1]
            except :
                tss = ts
            return render_template('reciept.html', d_flag=d_flag, C_list=C_list, U_list=U_list, CC=CC, cvalue=flask_login.current_user, bvalue=book.query.filter_by(book_id=got_book_id).first(), pvalue=tss)
        else :
            flash('Entered CATCHA doesnt match')
            return render_template("payment.html", values=book.query.filter_by(book_id=int(got_book_id)).all(), random_num=y, total_price=total_price)

@app.route('/store', methods=['POST','GET'])
def store() :
    if request.method == "POST" :
        if request.form['submit'] == "dashboard" :
            return render_template('customerdashboard.html')

@app.route('/logout', methods=['POST', 'GET'])
def mylogout() :
    flash('logged out successfully!')
    return render_template('mylogin.html')

@app.route('/fetchadm')
def fetchadmin1():
    return render_template("adminform.html")

@app.route('/fetchadmin', methods=["POST", "GET"])
def fetchadmin():
    if request.method == "POST":
        if request.form.get('button') == "Submit":
            book_id = request.form.get('book_id')
            customer_id = request.form.get('customer_id')
            delivery = request.form.get('delivery_status')
            transaction_id = request.form.get('transaction_id')
            if book_id == '' or customer_id == '' or delivery == '' or transaction_id == '':
                flash("you must enter all fields")
                return render_template("adminform.html")
            else:
                payment.query.filter_by(book_id = int(book_id), customer_id=int(customer_id), transaction_id=int(transaction_id)).update(dict(delivery=delivery))
                db.session.commit()
                flash('Status changed successfully!')
                return render_template("adminform.html")
        elif request.form.get("button") == "Back":
            return render_template("admindashboard.html")

if __name__ == "__main__":
    db.create_all(app=app)
    app.run()

