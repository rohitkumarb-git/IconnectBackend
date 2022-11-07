from flask import jsonify,request
from pymongo import MongoClient
import uuid

#Database
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
db = client.SelfEnrollmentData


class Meetings:
    def meeting_scheduling(self):
        agent={
            "_id":uuid.uuid4().hex,
            "agent_id":request.get_json()["agent_id"],
            "user_id":request.get_json()["user_id"],
            "meeting_details":request.get_json()["meeting_details"],
        }
        
        if db.agent_scheduled_meetings.insert_one(agent):
            return jsonify({"message":"Meeting Scheduled","agent_id":agent["agent_id"]}),200

        return jsonify({"error":"Meeting Scheduling Failed"}),200 
    def agent_meetings(self,agent_id):
        meeting_list=list(db.agent_scheduled_meetings.find({"agent_id":agent_id}))
        print(meeting_list)
        return meeting_list
    def agent_meetings_for_day(self,agent_id,date):
        meeting_list=list(db.agent_scheduled_meetings.find({"agent_id":agent_id}))
        meeting_list_for_day=[]
        for meeting in meeting_list:
            print(meeting)
            if meeting["meeting_details"]["scheduled_date"]==date:
                meeting_list_for_day.append(meeting)
        print(meeting_list_for_day)
        return jsonify(meeting_list_for_day)
        
