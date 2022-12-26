from flask import jsonify,request
from pymongo import MongoClient
import uuid,math,random

#Database
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
db = client.test

class Stories:
    #User Signup
    def getStory(self):
        stories_count=db.agents_profile.count_documents({})
        story=db.test.find().limit(1).skip(math.floor(random.random() * stories_count)).next()
        return jsonify({"story":story['story']}),200

    
class User_Story:
    # Function to save user response to DB
    def user_response(self):
        response={
            "_id":uuid.uuid4().hex,
            "story":request.get_json()["story"],
        }
        if db.user_responses.insert_one(response):
            return jsonify({"message":"User Story Saved to DataBase","response_id":response["_id"]})
