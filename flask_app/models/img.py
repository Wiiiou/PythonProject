from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import database


class Img:
    def __init__(self,data) -> None:
        self.id=data['id']
        self.file=data['file']
        self.condidate_id=data['condidate_id']
    @classmethod
    def save(cls,data):
        query="""INSERT INTO images(file,condidate_id)
                VALUES (%(file)s,%(condidate_id)s);"""
        return connectToMySQL(database).query_db(query,data)
    @classmethod
    def get_img_by_candidate_id(cls,data):
        query="""SELECT * FROM images 
                WHERE condidate_id = %(condidate_id)s and id=%(id)s;"""
        db_result=connectToMySQL(database).query_db(query,data)
        if db_result:
            return cls(db_result[0])
        return None
    @classmethod
    def update(cls,data):
        print(data['condidate_id'])
        query="""UPDATE images SET file=%(file)s WHERE
        condidate_id = %(condidate_id)s and id=%(id)s;"""
        db_result=connectToMySQL(database).query_db(query,data)
        return db_result
    @staticmethod
    def validate(data):
        is_valid=True
        print(data)
        if data['file']=="":
            is_valid=False
            flash('pls insert the link for the candidate')
        return is_valid
    