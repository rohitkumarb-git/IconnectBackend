from flask import jsonify,request
from pymongo import MongoClient
import uuid

#Database
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
db = client.SelfEnrollmentData

class User:
    def signup(self):
        # print(request.form)
        user={
            "_id":uuid.uuid4().hex,
            "name":request.get_json()['name'],
            "email":request.get_json()['email'].lower(),
            "password":request.get_json()['password']
        }
        if db.users.find_one({"email":user["email"]}):
            return  jsonify({"message":"Email address already exists, please login"}),400
        
        if db.users.insert_one(user):
            return jsonify({"message":"User Signed Up","user_id":user["_id"]})

        return jsonify({"error":"Signup Failed"}),400
    def login(self):
        user={
            "username":request.get_json()["username"],
            "password":request.get_json()["password"]
        }
        if db.users.find_one({"email":user["username"]}):
            password= db.users.find_one({"email":user["username"]})["password"]
            if password==user["password"]:
                return jsonify({"message":"User LoggedIn","token":db.users.find_one({"email":user["username"]})["_id"]})
        if not db.users.find_one({"email":user["username"]}):
            return jsonify({"message":"User does not exist, Please Signup"}),400
        return jsonify({"message":"Username or Password is incorrect"}),400
        