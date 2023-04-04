from flask import render_template,session, request,redirect,url_for,flash,current_app
from flask_login import login_required, current_user,login_user,logout_user
from shop import app,db,photos, search
from .models import Addproduct
from .forms import Addproducts
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import secrets
import os
from .imgMatcher import ImgMatcher
from .featuresext import Descriptor
from numpy import save


@app.route('/',methods=['GET','POST'])
def home():
    # page = request.args.get('page',1, type=int)
    # products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html')

@app.route('/trending')
def trending():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/trending.html', products=products)

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=6)
    return render_template('products/result.html',products=products)

@app.route('/imgresult', methods=['GET','POST'])
def imgresult():
    queryImg = request.files.get('image')
    imgName = secure_filename(queryImg.filename)
    if imgName=="":
        return redirect(url_for("home"))
    queryImg = queryImg.save(os.path.join(current_app.root_path,"static/searchImages/"+imgName))
    queryImg = ImgMatcher(imgName)
    cresults=queryImg.csearch()
    gresults=queryImg.gsearch()
    i=0
    j=0
    l=[]
    n=len(cresults)
    m=len(gresults)
    print(cresults)
    print(gresults  )
    while(i<n and j<m):
        x,y=cresults[i]
        if(x[0] not in l):
            l.append(x[0])
        x,y=gresults[j]
        if(x[0] not in l):
            l.append(x[0])
        i+=1
        j+=1
    displayproducts=[]
    for i in range(len(l)):
        x=Addproduct.query.filter(Addproduct.nparr.in_(l[i:i+1])).first()
        displayproducts.append(x)
    print(displayproducts)
    return render_template('products/imgresult.html',products=displayproducts)


@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product)

@app.route('/addproduct', methods=['GET','POST'])
@login_required
def addproduct():
    form = Addproducts(request.form)
    if request.method=="POST"and 'image_1' in request.files:
        name = form.name.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        sdesl =form.racklocation.data
        saddress= form.address.data
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        nparr=(image_1.split('.')[0])+".npy"
        d=Descriptor((8,12,13))
        des=d.grayFeatures(os.path.join(current_app.root_path, "static\\images\\"+image_1))
        save(os.path.join(current_app.root_path, 'static\\nparrs\\'+nparr),des)
        des=d.colorDescribe(os.path.join(current_app.root_path, "static\\images\\"+image_1))
        save(os.path.join(current_app.root_path, "static\\cnparrs\\"+nparr),des)
        addproduct = Addproduct(name=name,stock=stock,colors=colors,desc=desc,sdesl=sdesl,saddress=saddress,image_1=image_1,userId=current_user.id,nparr=nparr)
        db.session.add(addproduct)
        flash(f'The product {name} was added in database','success')
        db.session.commit()
        return render_template('products/addproduct.html', form=form)
    return render_template('products/addproduct.html', form=form)




@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        product.name = form.name.data 
        product.stock = form.stock.data 
        product.colors = form.colors.data
        product.desc = form.discription.data
        product.sdesl = form.racklocation.data
        product.saddress = form.address.data
        product.userId= current_user.id
        if request.files.get('image_1'):
            d=Descriptor((8,12,13))
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/nparrs/"+product.nparr))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
                des=d.grayFeatures(product.image_1)
                product.nparr = product.image_1.split('.')[0]+'npy'
                save(os.path.join(current_app.root_path,"static/nparr/"+product.nparr),des)
                des=d.colorDescribe(os.path.join(current_app.root_path, "static/images/"+product.image_1))
                save(os.path.join(current_app.root_path, "static/cnparr/"+product.nparr),des)

            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
                des=d.grayFeatures(product.image_1)
                product.nparr = product.image_1.split('.')[0]+'.npy'
                save(os.path.join(current_app.root_path,"static/nparr/"+product.nparr),des)
        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('home'))
    form.name.data = product.name
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.discription.data = product.desc
    return render_template('products/addproduct.html', form=form, title='Update Product',getproduct=product)

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))
