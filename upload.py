import os
from database import Database
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'image')

def upload_company(form, file):
    db = Database('Company')
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    cur = db.get_all_doc()
    id_number = cur.count() + 1
    doc = {
        'id': id_number,
        'name': form.name.data,
        'image': filename,
        'script': form.script.data
        }
    return db.upload_doc(doc)
    
    
def upload_product(form, file):
    db = Database('Product')
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    cur = db.get_all_doc()
    id_number = cur.count() + 1
    doc = {
        'id': id_number,
        'company_id': form.company_id.data,
        'name': form.name.data,
        'image': filename,
        'script': form.script.data
        }
    return db.upload_doc(doc)
    