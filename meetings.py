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
            return jsonify({"message":"Meeting Scheduled","agent_id":agent["agent_id"]})

        return jsonify({"error":"Meeting Scheduling Failed"}),400
        
