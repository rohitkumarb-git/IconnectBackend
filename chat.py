from flask import jsonify,request
from pymongo import MongoClient
import uuid,math,random

#Database
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
chat_db = client.ChatBox
selfEnrollment_db=client.SelfEnrollmentData


class Chat:

    def saveChatToDB(self):
        message={
            "_id":uuid.uuid4().hex,
            "sender":request.get_json()['from'],
            "reciever":request.get_json()['to'].lower(),
            "agent_id":request.get_json()['agent_id'],
            "user_id":request.get_json()['user_id'],
            "message":request.get_json()['message'],
            "date":request.get_json()['date'], #2022-12-21 Date format
            "time":request.get_json()['time'] #%I-%M-%S %p Time Format
        }
        # message={
        #     "name":"Rohit",
        #     "agent_id":"2746347623412875",
        #     "user_id":"35238342353299419"
        # }
        collection_name=str(message["agent_id"])+"_"+str(message["user_id"])
        if chat_db[collection_name].insert_one(message):
            return {"message":"Message Saved to DB"},200
        
    def getChatfromDB(self):
        message={"agent_id":request.get_json()["agent_id"], "user_id":request.get_json()["user_id"]}
        collection_name=message["agent_id"]+"_"+message["user_id"]
        chat=list(chat_db[collection_name].find())
        return chat,200

    def getChattedUsers(self):
        agent_id= request.get_json()["agent_id"]
        collection_list=[]
        user_id_list=[]
        users_list=[]
        for collection_name in chat_db.list_collection_names():
         if collection_name.startswith(agent_id):
            collection_list.append(collection_name)
        for collection_id in collection_list:
            user_id_list.append(collection_id.split("_")[1])
        for id in user_id_list:
            user=selfEnrollment_db.users.find_one({"_id":id})
            users_list.append({"user_id":user["_id"],"user_name":user["name"]})
        # print(users_list)
        return(users_list)
        
    
# rohit=Chat()
# rohit.getAgentChatList()
# rohit.getChattedUsers(agent_id="cb81749e345149719aaab1efb9141259")
# rohit.getChatfromDB(agent_id="2746347623412875",user_id="35238342353299419")

# def getAgentChatList():
#         # agent_id= request.get_json()["agent_id"]
#         agent_id="cb81749e345149719aaab1efb9141259"
#         list_of_collections= list(chat_db.list_collection_names())
#         # print(list_of_agent_collections)
#         list_of_agent_collections=[]
#         for collection_name in list_of_collections:
#             print(collection_name)
#             if collection_name.startswith(agent_id):
#                 list_of_agent_collections.append(collection_name)
#                 print(list_of_agent_collections)
#         return list_of_agent_collections
# getAgentChatList()