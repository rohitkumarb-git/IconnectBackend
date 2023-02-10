from flask import jsonify,request, json
from pymongo import MongoClient
import uuid,math,random

#Database
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
# chat_db = client.ChatBox
db=client.SelfEnrollmentData


class CallHistroy:

    def saveCallHistoryToDB(self):
        message={
            "_id":uuid.uuid4().hex,
            "agent_id":request.get_json()['agent_id'],
            "user_id":request.get_json()['user_id'],
            "date":request.get_json()['date'], #2022-12-21 Date format
            "time":request.get_json()['time'] #%I-%M-%S %p Time Format
        }
        # message={
        #     "name":"Rohit",
        #     "agent_id":"2746347623412875",
        #     "user_id":"35238342353299419"
        # }
        # collection_name=str(message["agent_id"])+"_"+str(message["user_id"])
        if db.agents_call_history.insert_one(message):
            return {"message":"Call History Saved to DB"},200
        
    def getAgentCallHistoryfromDB(self, agent_id):
        # agent_id=request.get_json()["agent_id"], 
        # user_id=request.get_json()["user_id"]
        callhistory=list(db.agents_call_history.find({"agent_id":agent_id}))
        user_id_list=list(set([log["user_id"] for log in callhistory]))
        user_list=[]
        for i in user_id_list:
            print(i)
            userdetails=list(db.users.find({"_id":i}))
            user_list.append(userdetails[0])
        # print(user_list)
        # print(callhistory)
        return user_list,200

a= CallHistroy()
a.getAgentCallHistoryfromDB("cb81749e345149719aaab1efb9141259")
