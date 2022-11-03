from bson.objectid import ObjectId
from flask import Flask,request
from pymongo import MongoClient
from flask_cors import CORS,cross_origin
import math,random


app= Flask(__name__)
CORS(app)
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
# define the database to use
db = client.SelfEnrollmentData

#Backend Home Page
@app.route("/",methods=["GET"])
def home():
    return "Welcome to iConnect Backend URL"

#Fecth User Details From DB
@app.route("/user",methods=["GET"])
def users():
    users_count=db.users.count_documents({})
    user=db.users.find().limit(1).skip(math.floor(random.random() * users_count)).next()
    print(user)
    return user["name"]

# Fecth Questions From DB
@app.route("/questions",methods=["GET"])
def questions():
    a= db.questions.find_one()
    return a['questions']

#Post User Response to DB
@app.route("/response",methods=["POST"])
def response():
    data={}
    if request.method=="POST":
        users_count=db.users.count_documents({})
        user=db.users.find().limit(1).skip(math.floor(random.random() * users_count)).next()
        data["user_id"]=str(user["_id"])
        data["user_response"]=request.get_json()
        a=db.user_responses.insert_one(data)
        return str(a.inserted_id)

#Fecth Agent From DB
@app.route("/available_agent",methods=["GET"])
def agents():
    agents_count=db.agents_profile.count_documents({})
    agent=db.agents_profile.find().limit(1).skip(math.floor(random.random() * agents_count)).next()
    print(agent)
    return str(agent["_id"])

#Post Scheduled Meetings to DB
@app.route("/agent_meeting_scheduling",methods=["POST","GET"])
def meeting_scheduling():
    data={}
    if request.method=="POST":
        data["user_id"]=request.get_json()["user_id"]
        # print(data)
        data["agent_id"]=request.get_json()["agent_id"]
        data["meeting_details"]=request.get_json()["meeting_details"]
        # print(data)
        a=db.agent_scheduled_meetings.insert_one(data)
        return str(a.inserted_id)
    elif request.method=="GET":
        meetings=db.agent_scheduled_meetings.find({})
        return "No. of Pending Meetings are %s", len(meetings)


if __name__=="__main__":
    app.run(debug=True)
