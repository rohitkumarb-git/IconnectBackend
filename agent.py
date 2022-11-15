from flask import jsonify,request
from pymongo import MongoClient
import uuid

#Database
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
db = client.SelfEnrollmentData


class Agent:
    def signup(self):
        print(request.form)
        agent={
            "_id":uuid.uuid4().hex,
            "name":request.form.get('name'),
            "email":request.form.get('email').lower(),
            "password":request.form.get('password')
        }

        if db.agents.find_one({"email":agent["email"]}):
            return  jsonify({"message":"Email address already in use"})
        
        if db.agents.insert_one(agent):
            return jsonify({"message":"Agent Signed Up","agent_id":agent["_id"]})

        return jsonify({"error":"Signup Failed"})
    def login(self):
        agent={
            "username":request.form.get("username"),
            "password":request.form.get("password")
        }
        if db.agents.find_one({"email":agent["username"]}):
            password= db.agents.find_one({"email":agent["username"]})["password"]
            if password==agent["password"]:
                return jsonify({"message":"Agent LoggedIn","token":db.agents.find_one({"email":agent["username"]})["_id"]})
        if not db.agents.find_one({"email":agent["username"]}):
            return jsonify({"message":"User does not exist, Please Signup"})
        return jsonify({"message":"Username or Password is incorrect"})
        