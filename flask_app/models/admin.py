from flask import flash
from flask_app import database
from flask_app.config.mysqlconnection import connectToMySQL

import re
email_regex=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Admin:
    def __init__(self,data):
        self.id=data['id']
        self.username=data['username']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
    
    @classmethod
    def get_admin_by_email(cls,data):
        query="""SELECT * FROM admins WHERE email=%(email)s;"""
        db_result=connectToMySQL(database).query_db(query,data)
        if db_result<1:
            return False
        return True
    @staticmethod
    def validate(data):
        is_valid=True
        if not email_regex.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if data['email']!="fakroun@gmail.com":
            is_valid=False
            flash('your Email is invalid so pls renter your email',"login")
        if data['password']!="fakroun123":
            flash('your Password is Wrong so Please valid your password',"login")
            is_valid=False
        return is_valid