# -*- coding: utf-8 -*-
from database import Database
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Required, EqualTo, length, Regexp

class UploadCompany(FlaskForm):
    name = StringField('name of the company', 
        validators=[Required(), Regexp('^[A-Za-z][A-Za-z0-9_]*$',
        0, 'name must have only letters, numbers, dots or underscores')])
    script = StringField('script of the company', validators=[length(max=300)])
    file = FileField('Image', [FileRequired()])
    submit_company = SubmitField('Submit')
    
class UploadProduct(FlaskForm):
    name = StringField('name of the product', 
        validators=[Required(), Regexp('^[A-Za-z][A-Za-z0-9_]*$',
        0, 'name must have only letters, numbers, dots or underscores')])
    company_id = SelectField('company',coerce=int, validators=[DataRequired()])
    script = StringField('script of the product', validators=[length(max=300)])
    file = FileField('Image', [FileRequired()])
    submit_product = SubmitField('Submit')
    def __init__(self):
        super(UploadProduct, self).__init__()
        db = Database('Company')
        self.company_id.choices = [(doc['id'], doc['name'])
            for doc in db.get_all_doc()]