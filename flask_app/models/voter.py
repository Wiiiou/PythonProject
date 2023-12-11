from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import database
from flask import flash
from flask_app import app

import re
email_regex=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Voter:
    def __init__(self ,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.cin=data['cin']#for id number
        self.region=data['region']
        self.vote=data['vote']
        self.age=data['age']
        self.password=data['password']
        self.is_banned = data['is_banned']
    @classmethod
    def create(cls,data):
        query="""INSERT INTO voters
        (first_name,last_name,email,password,age,region,cin,vote,is_banned) VALUES
                (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(age)s
                ,%(region)s,%(cin)s,0,0);"""
        return connectToMySQL(database).query_db(query,data)
    
    @classmethod
    def vote(cls,data):
        query="""INSERT INTO votes
        (vote_id,condidate_id) VALUES
                (%(vote_id)s,%(condidate_id)s);"""
        return connectToMySQL(database).query_db(query,data)
        

    @classmethod
    def get_all(cls):
        query="""SELECT * FROM voters;"""
        db_result=connectToMySQL(database).query_db(query)
        all_voters=[]
        for row in db_result:
            all_voters.append(row)
        return all_voters
    @classmethod
    def get_voter_by_email(cls,data):
        query="""SELECT * FROM voters WHERE email =%(email)s;"""
        db_result=connectToMySQL(database).query_db(query,data)
        if db_result:
            return cls(db_result[0])
        return None
    @staticmethod
    def update(data):
        query="""
            UPDATE voters SET is_banned=%(x)s WHERE id=%(id)s;
            """ 
        return connectToMySQL(database).query_db(query,data)
    @staticmethod
    def validate(data):
        is_valid=True
        countM=0
        countm=0
        countnumber=0
        if len(data['first_name'])<3 or len(data['last_name'])<3:
            is_valid=False
            flash('please enter a valid first_name and last_name mean too short')
        if not email_regex.match(data['email']):
            is_valid=False
            flash('your email is invalid')
        if data['region']=="Select your region":
            is_valid=False
            flash('please select your region')
        if data['birthdate']=="":
            is_valid=False
            flash('please insert your birthday')
        if len(data['password'])<8:
            for i in range(len(data['password'])):
                if "A"<data['password'][i]<"Z":
                    countM+=1
                elif "a"<data['password'][i]<"z":
                    countm+=1
                else:
                    countnumber+=1
            if countM==0 or countm==0:
                is_valid=False
                flash('Must contain at least one Upper Case and one Camel Case and one number')
        for i in range(len(Voter.get_all())):
            print(Voter.get_all()[i])
            print(Voter.get_all()[i]['cin'])
            print(data['cin'])
            if data['cin'] == Voter.get_all()[i]['cin']:
                is_valid=False
                flash('this Id already Exit')
                print(is_valid)
                break
        return is_valid     
