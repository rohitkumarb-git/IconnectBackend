import math,random
from datetime import timedelta,datetime,date
from flask import Flask,jsonify,request
from pymongo import MongoClient
from flask_cors import CORS
from agent import Agent
from user import User,User_Response
from meetings import Meetings
from chat import Chat
from callhistory import CallHistroy



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
@app.route("/available_agent",methods=["POST"])
def agents():
    agent=Agent()
    return agent.agentAvailability()

# Fecth Questions From DB
@app.route("/questions",methods=["GET"])
def questions():
    a= db.questions.find_one()
    return jsonify(a["survey"])

#Post User Response to DB
@app.route("/response",methods=["POST"])
def response():
    user=User_Response()
    return user.user_response()


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

#Route for all Scheduled Meetings for an Agent
@app.route("/agent_meetings/<agent_id>",methods=["GET"])
def agent_meetings(agent_id):
    agent_meetings=Agent()
    return agent_meetings.agent_meetings(agent_id)

#Route for all Scheduled Meetings for Agent for Particular day
@app.route("/agent_meetings/<agent_id>/<date>",methods=["GET"])
def agent_meetings_for_day(agent_id,date):
    agent_meetings=Agent()
    return agent_meetings.agent_meetings_for_day(agent_id,date)

# Route to get Upcoming 30Days Meetings for particular agent
@app.route("/agent_upcoming_meetings/<agent_id>", methods=["GET"]) #date: 2022-12-20 (todays date)
def agent_upcoming_meetings(agent_id):
    user_date= date.today()
    # user_date=datetime.strptime("2022-12-01","%Y-%m-%d")
    upcoming_date=""
    meetings=[]
    for i in range(1,31):
        upcoming_date=user_date+timedelta(i)
        date_string=upcoming_date.strftime('%Y-%m-%d')
        agent_meetings=Agent()
        day_meetings=agent_meetings.agent_meetings_for_day(agent_id,date_string)
        if len(day_meetings)!=0:
            meetings.append(day_meetings)
    return meetings

# Route to get Previous 30Days Meetings for particular agent
@app.route("/agent_previous_meetings/<agent_id>", methods=["GET"]) #date: 2022-12-20 (todays date)
def agent_previous_meetings(agent_id):
    user_date= date.today()
    # user_date=datetime.strptime("2022-12-01","%Y-%m-%d")
    upcoming_date=""
    meetings=[]
    for i in range(1,31):
        previous_date=user_date-timedelta(i)
        # print(previous_date)
        date_string=previous_date.strftime('%Y-%m-%d')
        agent_meetings=Agent()
        day_meetings=agent_meetings.agent_meetings_for_day(agent_id,date_string)
        if len(day_meetings)!=0:
            meetings.append(day_meetings)
    return meetings

# Route for Agent Available Slots
@app.route("/agent_available_slots/<agent_id>/<date>", methods=["GET"])
def agent_slots(agent_id,date):
    agent_slots= Agent()
    return agent_slots.agentAvailabileSlots(agent_id,date)


#Route to Save Chat & Get Chat from DB
@ app.route("/agent_user_chat",methods=["GET", "POST"])
def agentUserChat():
    agent_user_chat=Chat()
    if request.method=="GET":
        return agent_user_chat.getChatfromDB()
    elif request.method=="POST":
        return agent_user_chat.saveChatToDB()

#Route to fetch users chatted with Particular agent
@app.route("/get_chatted_users", methods=["POST"])
def fecthUsersChattedWithAgent():
    get_Chatted_Users=Chat()
    return get_Chatted_Users.getChattedUsers()


# Route to save call history to DB
@app.route("/save_agents_call_history", methods=["POST"])
def saveAgentCallHistory():
    save_Call_History=CallHistroy()
    return save_Call_History.saveCallHistoryToDB()

# Route to get Agent Call History
@app.route("/agent_call_history/<agent_id>", methods=["GET"])
def getAgentCallHistory(agent_id):
    get_Call_History=CallHistroy()
    return get_Call_History.getAgentCallHistoryfromDB(agent_id)

if __name__=="__main__":
    app.run(debug=True)
