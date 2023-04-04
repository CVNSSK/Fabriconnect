from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import app,db,bcrypt,photos
from .forms import RegistrationForm,LoginForm
from shop.shopkeeper.models import Register
from .models import Admins
import os

def getshopkeepers():
    shopkeepers = Register.query.all()
    return shopkeepers

def isLogged():
    try:
        if (Admins.query.filter_by(email=session['email']).first()).email==session['email']:
            return True
        return False
    except:
        return False

@app.route('/admin')
def admin():
    if isLogged():
        shopkeepers=getshopkeepers()
        return render_template('admin/index.html', title='Admin page',shopkeepers=shopkeepers)
    return redirect('login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        # profilepic = photos.save(request.files.get('profile'), name=secrets.token_hex(10) + ".")
        admins = Admins(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password,role='admin')
        db.session.add(admins)
        flash(f'welcome {form.name.data} Thanks for registering','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html',title='Register Admin', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admins.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            session['email'] = form.email.data
            session['name']=admin.name
            flash(f'welcome {form.email.data} you are logedin now','success')
            next = request.args.get('next')
            return redirect(url_for(next or 'admin'))
        else:
            flash(f'Wrong email and password', 'danger')
            return redirect(url_for('login'))
    return render_template('admin/login.html',title='Login page',form=form)

@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('name',None)
    return redirect('login')

@app.route('/deleteshopkeeper/<int:id>', methods=['POST'])
def deleteshopkeeper(id):
    if isLogged():
        shopkeeper = Register.query.get_or_404(id)
        if request.method =="POST":
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + shopkeeper.profile))
            except Exception as e:
                print(e)
            db.session.delete(shopkeeper)
            db.session.commit()
            flash(f'The product {shopkeeper.name} was delete from your record','success')
            return redirect(url_for('admin'))
        flash(f'Can not delete the shopkeeper','danger')
        return redirect(url_for('admin'))
    else:
        return redirect('login')