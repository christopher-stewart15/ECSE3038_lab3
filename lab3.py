from flask import Flask , request, jsonify,json
from flask_pymongo import PyMongo
from marshmallow import Schema , fields , ValidationError
from bson.json_util import dumps
from json import loads
from datetime import datetime

app = Flask (__name__)
app.config ["MONGO_URI"] = "mongodb+srv://nashhq:N.hamilton@cluster0.7pkmk.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)


Test_Num = 0


profile_DB = {
    "sucess": True,
    "data": {
        "last_updated": "2/3/2021, 8:48:51 PM",
        "username": "Christopher Stewart",
        "role": "Electronics Engineer",
        "color": "Blue"
    }
}



class TankSchema(Schema):
    location = fields.String(required=True)
    latitude  = fields.String(required=True)
    longitude = fields.String(required=True)
    percentage_full = fields.Integer(required=True)

############################################################
# routes for profile

@app.route("/")
def home():
    return "Welcome to the home page!"

@app.route("/profile", methods=["GET", "POST", "PATCH"])
def profile():
    if request.method == "POST":
       
        profile_DB["data"]["last_updated"] = (dte.strftime("%c"))
        profile_DB["data"]["username"] = (request.json["username"])
        profile_DB["data"]["role"] = (request.json["role"])
        profile_DB["data"]["color"] = (request.json["color"])
       
        return jsonify(profile_DB)
   
    elif request.method == "PATCH":
        
        profile_DB["data"]["last_updated"] = (dte.strftime("%c"))
        
        x = request.json
        attributes = x.keys()
        
        for attribute in attributes:
            profile_DB["data"][attribute] = x[attribute]
  
        return jsonify(profile_DB)

    else:
        
        return jsonify(profile_DB)


#############################################################################
# routes for tank

@app.route("/tank")
def get_tank ():
    tanks = mongo.db.fruits.find()
    return jsonify(loads(dumps(tanks)))

@app.route ("/tank", methods = ["POST"])
def add_Tank ():
    try:
        newTank = TankSchema().load(request.json)
        tank_id = mongo.db.fruits.insert_one(newTank).inserted_id
        tank = mongo.db.fruits.find_one(tank_id)
        return loads(dumps(tank))
    except ValidationError as ve:
         return ve.messages, 400

@app.route ("/tank/<ObjectId:id>", methods = ["PATCH"])
def update_tank(id):
    mongo.db.fruits.update_one({"_id": id}, {"$set": request.json})
    tank = mongo.db.fruits.find_one(id)
    return loads(dumps(tank))

@app.route ("/tank/<ObjectId:id>", methods = ["DELETE"])
def delete_tank(id):
    result = mongo.db.fruits.delete_one({"_id": id})
    if result.deleted_count == 1:
       return {
           "Success": True
        }
    else:
        return {
               "Success": False
            }, 400





if __name__ =="__main__" :
    app.run (port=3000, debug = True )