import math,random
from flask import Flask,jsonify
from pymongo import MongoClient
from flask_cors import CORS
from agent import Agent
from user import User
from meetings import Meetings
from user_response import User_Response

app= Flask(__name__)
CORS(app)

#Database
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
db = client.SelfEnrollmentData

#Routes
#Backend Home Page
@app.route("/",methods=["GET"])
def home():
    return "Welcome to iConnect Backend URL"

#Fecth Random User Details From DB
@app.route("/user",methods=["GET"])
def users():
    users_count=db.users.count_documents({})
    user=db.users.find().limit(1).skip(math.floor(random.random() * users_count)).next()
    return user["_id"]

#Fecth Random Agent From DB
@app.route("/available_agent",methods=["GET"])
def agents():
    agents_count=db.agents_profile.count_documents({})
    agent=db.agents_profile.find().limit(1).skip(math.floor(random.random() * agents_count)).next()
    print(agent)
    return str(agent["_id"])

# Fecth Questions From DB
@app.route("/questions",methods=["GET"])
def questions():
    a= db.questions.find_one()
    return jsonify(a["survey"])

#Post User Response to DB
@app.route("/response",methods=["POST"])
def response():
    response=User_Response()
    return response.user_response()


#User Signup Route
@app.route('/user_signup',methods=['POST'])
def user_signup():
    user=User()
    return user.signup()

# User Enrollment Route
@app.route('/user_enroll',methods=['POST'])
def user_enroll():
    user=User()
    return user.userEnrollment()

#User Login Route
@app.route("/user_login",methods=["POST"])
def user_login():
    user=User()
    return user.login()


#Agent Signup Route
@app.route('/agent_signup',methods=['POST'])
def agent_signup():
    agent=Agent()
    return agent.signup()

#Agent Login Route
@app.route("/agent_login",methods=["POST"])
def agent_login():
    agent=Agent()
    return agent.login()

# Agent Profile Route
@app.route("/agent_profile/<agent_id>",methods=["GET"])
def getAgentProfile(agent_id):
    agent_profile=Agent()
    return agent_profile.getAgentProfile(agent_id)

#Meeting Scheduling Route
@app.route("/meeting_scheduling",methods=["POST"])
def meeting_scheduling():
    meeting_scheduling=Meetings()
    return meeting_scheduling.meeting_scheduling()

#All Scheduled Meetings for Agent Route
@app.route("/agent_meetings/<agent_id>",methods=["GET"])
def agent_meetings(agent_id):
    agent_meetings=Agent()
    return agent_meetings.agent_meetings(agent_id)

#All Scheduled Meetings for Agent for particular day Route
@app.route("/agent_meetings/<agent_id>/<date>",methods=["GET"])
def agent_meetings_for_day(agent_id,date):
    agent_meetings=Agent()
    return agent_meetings.agent_meetings_for_day(agent_id,date)

@app.route("/agent_available_slots/<agent_id>/<date>", methods=["GET"])
def agent_slots(agent_id,date):
    agent_slots= Agent()
    return agent_slots.agentAvailability(agent_id,date)

if __name__=="__main__":
    app.run(debug=True)
