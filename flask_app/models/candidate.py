from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import database
from flask import flash
from flask import jsonify

import re
email_regex=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Candidate:
    def __init__(self ,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.bio=data['bio']#for id number
        self.region=data['region']
        self.age=data['age']
        self.password=data['password']
        # self.candidate_id=data['candidate_id']
    @classmethod
    def create(cls,data):
        query="""INSERT INTO condidates
        (first_name,last_name,email,password,age,region,bio) VALUES
                (%(first_name)s,%(last_name)s,%(email)s,%(password)s
                ,%(age)s,%(region)s,%(bio)s);"""
        return connectToMySQL(database).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query="""SELECT * FROM condidates;"""
        db_result=connectToMySQL(database).query_db(query)
        all_voters=[]
        for row in db_result:
            all_voters.append(row)
        return all_voters
    @classmethod
    def get_voter_by_email(cls,data):
        query="""SELECT * FROM condidates WHERE email =%(email)s;"""
        db_result=connectToMySQL(database).query_db(query,data)
        if db_result:
            return cls(db_result[0])
        return None
    @classmethod
    def get_candidate_by_id(cls,data):
        query="""SELECT * FROM condidates WHERE id=%(id)s;"""
        db_result=connectToMySQL(database).query_db(query,data)
        print(db_result, data)
        if db_result:
            return cls(db_result[0])
        return None
    
    @classmethod
    def get_candidate_votes(cls, data):
        print(data)
        query = "SELECT COUNT(*) AS vote_count,region FROM votes WHERE condidate_id =%(id)s group by region;"
        db_result = connectToMySQL(database).query_db(query, data)
        print(db_result)
        if db_result:
            return db_result
        return None
    
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
        if data['age']=="" or int(data['age'])<18:
            is_valid=False
            flash('please insert your age and must be 18 years old')
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
        if len(data['bio'])<10:
            flash('the bio must be at least 10 string long')
            is_valid=False
        for i in range(len(Candidate.get_all())):
            print(Candidate.get_all()[i])
            print(Candidate.get_all()[i]['email'])
            if data['email']==Candidate.get_all()[i]['email']:
                is_valid=False
                flash('email already exist so pls try another one ')
                break
        return is_valid