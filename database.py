# -*- coding: utf-8 -*-

from models import Models
from pymongo import MongoClient

DATABASE_URI = "mongodb://localhost:27017/"

class Database(Models):
    
    def __init__(self, kind: str):
        #傳資料庫位址
        self.client = MongoClient(DATABASE_URI)
        self.kind = kind
        self.db = self.client[kind]

    '''
    目前格式
    example = {
        'name':  'name',
        'id': id -> int 
        'image': 'image_name'
        }
    }
    '''
    def get_all_doc(self):
        return self.db.doc.find()

    def get_doc_by_id(self, key: str, kind_id: str):
        try:
            cur = self.db.doc.find({key: int(kind_id)})
        except Exception as e:
            self.log("ERROR : " + str(e))
            return None
        if cur.count() != 0:
            return cur
        else:
            self.log("(kind: "+self.kind+", id: "+str(kind_id)+") doc is not found")
            return None
    
    def upload_doc(self, doc: dict):
        if self.db.doc.insert_one(doc):
            return True
        return False