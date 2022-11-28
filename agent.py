from flask import jsonify,request
from pymongo import MongoClient
import uuid,math,random

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
        
    def getAgentProfile(self,agent_id):
        return db.agents_profile.find_one({"_id":agent_id})
    
    def agent_meetings(self,agent_id):
        meeting_list=list(db.agent_scheduled_meetings.find({"agent_id":agent_id}))
        print(meeting_list)
        return meeting_list

    def agent_meetings_for_day(self,agent_id,date):
        meeting_list=list(db.agent_scheduled_meetings.find({"agent_id":agent_id}))
        meeting_list_for_day=[]
        for meeting in meeting_list:
            # print(meeting)
            if meeting["meeting_details"]["scheduled_date"]==date:
                meeting_list_for_day.append(meeting)
        # print(meeting_list_for_day)
        return jsonify(meeting_list_for_day)

    def agentAvailabileSlots(self,agent_id,date):
        agent_availability={"available_slots":["9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30"]}
        scheduled_slots=[]
        meetings_list= self.agent_meetings_for_day(agent_id,date).get_json()
        # print(meetings_list)
        for meeting in meetings_list:
            agent_availability["available_slots"].remove(meeting["meeting_details"]["scheduled_start_time"])
        return agent_availability
    
    def agentAvailability(self):
        
        user_id=request.get_json()['user_id']
        if db.user_agent_relation.find_one({"user_id":user_id}):
            agent_id=db.user_agent_relation.find_one({"user_id":user_id})["agent_id"]
            agent= db.agents_profile.find_one({"_id":agent_id})
            return agent
        else:
            agents_count=db.agents_profile.count_documents({})
            agent=db.agents_profile.find().limit(1).skip(math.floor(random.random() * agents_count)).next()
            agent_relation={"_id":uuid.uuid4().hex,
                            "agent_id":agent["_id"],
                            "user_id":user_id
                           }
            db.user_agent_relation.insert_one(agent_relation)
            return agent
