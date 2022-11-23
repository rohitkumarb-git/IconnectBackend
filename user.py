from flask import jsonify,request
from pymongo import MongoClient
import uuid

#Database
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
db = client.SelfEnrollmentData

class User:
    #User Signup
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
            return jsonify({"message":"User Signed Up","user_id":user["_id"],"user_name":user["name"]}),200

        return jsonify({"error":"Signup Failed"}),400

    #User Enrollment 
    def userEnrollment(self):
        # print(request.form)
        user={
            "_id":uuid.uuid4().hex,
            "name":request.get_json()['name'],
            "email":request.get_json()['email'].lower(),
            "phone":request.get_json()['phone']
        }
        # "password":request.get_json()['password']
        existing_user={}
        if db.users.find_one({"email":user["email"]}):
            if db.users.find_one({"phone":user["phone"]}):
                existing_user= db.users.find_one({"email":user["email"]})
                return  jsonify({"message":"User Already Exist", "user_id": existing_user["_id"], "user_name":existing_user["name"]}),200
#             return jsonify({"message":"Email Address already exists"}),400
        
        if db.users.insert_one(user):
            return jsonify({"message":"User Enrolled","user_id":user["_id"],"user_name":user["name"]}),200

        return jsonify({"error":"Signup Failed"}),400

    #User Login
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
        
