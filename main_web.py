# -*- coding: utf-8 -*-
from database import Database
from models import Models
import forms as fm
import upload as upld
from pymongo import MongoClient
from flask import Flask, render_template, session, redirect, url_for, flash, request, send_from_directory, send_file, abort
from flask_bootstrap import Bootstrap
import os
import io

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'projectkey'
app.config['IMAGE_FOLDER'] = os.path.join(os.path.dirname(__file__), 'image')
bootstrap = Bootstrap(app)
model = Models()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def homepage():
    db = Database('Company')
    kind_ids = []
    images = []
    for doc in db.get_all_doc():
        kind_ids.append(doc['id'])
        images.append(doc['image'])
    return render_template('homepage.html',kind='Company',
        kind_ids=kind_ids, images=images)


@app.route('/image/<kind>/<kind_id>', methods=['GET'])
def image(kind, kind_id):
    db = Database(kind)
    cur = db.get_doc_by_id(key='id', kind_id=kind_id)
    if cur is not None:
        for doc in cur:
            return send_from_directory(app.config['IMAGE_FOLDER'], doc['image'])
        return f"Nothing"
    else:
        model.log("(kind: "+kind+", id: "+str(kind_id)+") image is not found")
        abort(404)
 
 
@app.route('/product/<kind_id>', methods=['GET'])   
def product(kind_id):
    db = Database('Product')
    cur = db.get_doc_by_id(key='company_id',kind_id=kind_id)
    product_ids = []
    images = []
    if cur is not None:
        for doc in cur:
            product_ids.append(doc['id'])
            images.append(doc['image'])
    else:
        product_ids = None
        images = None
    return render_template('product.html',kind='Product',
        product_ids=product_ids, images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload_to_database():
    company_form = fm.UploadCompany()
    product_form = fm.UploadProduct()
    if company_form.submit_company.data and company_form.validate_on_submit():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if upld.upload_company(company_form, file):
                flash('Upload done')
                return redirect(request.url)
            else:
                flash('Upload fail')
                return redirect(request.url)
        else:
            flash('File not allowed')
            return redirect(request.url)
    if product_form.submit_product.data and product_form.validate_on_submit():
        print('2')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if upld.upload_product(product_form, file):
                flash('Upload done')
                return redirect(request.url)
            else:
                flash('Upload fail')
                return redirect(request.url)
        else:
            flash('File not allowed')
            return redirect(request.url)
    print('fail')
    return render_template('upload.html',
        company_form=company_form,product_form=product_form)

if __name__ == "__main__":
    app.run()