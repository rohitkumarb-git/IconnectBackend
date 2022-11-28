from flask import jsonify,request
from pymongo import MongoClient
import uuid,math,random

#Database
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
db = client.SelfEnrollmentData

class User_Response:
    def user_response(self):
        users_count=db.users.count_documents({})
        response={
            "_id":uuid.uuid4().hex,
            "user_id":request.get_json()["user_id"],
            "user_response":request.get_json()["user_response"]}
        if db.user_responses.insert_one(response):
            return jsonify({"message":"User Response Saved to DataBase","response_id":response["_id"]})