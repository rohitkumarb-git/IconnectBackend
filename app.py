from flask import Flask,request
from pymongo import MongoClient


app= Flask(__name__)
client = MongoClient('mongodb+srv://rohitkumar:Mongodb%4031@iconnect-cluster.kni459t.mongodb.net/?retryWrites=true&w=majority')
# define the database to use
db = client.SelfEnrollmentData

@app.route("/",methods=["GET"])
def home():
    return "Welcome to iConnect Backend URL"

@app.route("/questions",methods=["GET"])
def questions():
    a= db.questions.find_one()
    print(a['questions'])
    return a['questions']

@app.route("/response",methods=["POST","GET"])
def response():
    data={}
    if request.method=="POST":
        user=db.users.find_one()
        data["user_id"]=str(user["_id"])
        data["user_response"]=request.get_json()["user_response"]
        # print(data["user_response"])
        a=db.user_responses.insert_one(data)
        return str(a.inserted_id)
    elif request.method=="GET":
        return "Please POST Your Response"

if __name__=="__main__":
    app.run(debug=True)
