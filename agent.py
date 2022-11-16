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
        agent_profile={
            "_id":agent["_id"],
            "name":request.get_json()['name'],
            "email":request.get_json()['email'].lower(),
            "phone":request.get_json()['phone'],
            "place":request.get_json()['palce'],
            "about":request.get_json['about'],
            "image_url":request.get_json()['image_url'],
            "website":request.get_json()['website']
        }

        if db.agents.find_one({"email":agent["email"]}):
            if db.agents_profile.find_one({"email":agent["email"]}):
                return  jsonify({"message":"Email address already in use"}),400
        
        if db.agents.insert_one(agent):
            if db.agents_profile.insert_one(agent_profile):
                return jsonify({"message":"Agent Signed Up","agent_id":agent["_id"]})

        return jsonify({"error":"Signup Failed"}),400
    def login(self):
        agent={
            "username":request.get_json()["username"],
            "password":request.get_json()["password"]
        }
        if db.agents.find_one({"email":agent["username"]}):
            password= db.agents.find_one({"email":agent["username"]})["password"]
            if password==agent["password"]:
                return jsonify({"message":"Agent LoggedIn","token":db.agents.find_one({"email":agent["username"]})["_id"]})
        if not db.agents.find_one({"email":agent["username"]}):
            return jsonify({"message":"User does not exist, Please Signup"}),400
        return jsonify({"message":"Username or Password is incorrect"}),400
        
    def getAgentProfile(self,token):
        return db.agents_profile.find_one({"_id":token})
