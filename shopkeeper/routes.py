from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import app,db,photos, search,bcrypt,login_manager
from .forms import ShopkeeperRegisterForm, ShopkeeperLoginFrom
from .models import Register
# from shop.products.models import Addproduct
# from shop.products.forms import Addproducts
import secrets
import os
import json

buplishable_key ='pk_test_MaILxTYQ15v5Uhd6NKI9wPdD00qdL0QZSl'


@app.route('/shopkeeper/register', methods=['GET','POST'])
def shopkeeper_register():
    form = ShopkeeperRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data,state=form.state.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data, role="shopkeeper")
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('shopkeeperLogin'))
    return render_template('shopkeeper/register.html', form=form)


@app.route('/shopkeeper/login', methods=['GET','POST'])
def shopkeeperLogin():
    form = ShopkeeperLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'welcome {form.email.data} you are logedin now','success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))    
        flash('Incorrect email and password','danger')
        return redirect(url_for('shopkeeperLogin'))
    return render_template('shopkeeper/login.html', form=form)


@app.route('/shopkeeper/logout')
def shopkeeper_logout():
    logout_user()
    return redirect(url_for('home'))
