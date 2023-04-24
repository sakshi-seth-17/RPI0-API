'''
    Import necessary packages
'''
from flask import Flask, jsonify,request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import base64
from PIL import Image
from io import BytesIO
import requests
import json
from userdefined import *
import os

'''
    load required data
'''
configData = readJson("/var/www/aspendb/probesearch/rpi0/config.json")
#RPI_Details = readJson("/var/www/aspendb/probesearch/SensorsData/RPI-Details.json")

'''  firebase db-key  '''
cred = credentials.Certificate("/var/www/aspendb/probesearch/rpi0/db-key.json")

'''  initialize_app for firebase database '''
firebase_admin.initialize_app(cred)
db = firestore.client()

firebaseConfig = configData["firebaseConfig"]




'''  initialize app for flask '''
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}},support_credentials=True)
#app.config['CORS_HEADERS'] = 'Content-Type'
    
    
'''  root api to check connectivity '''
@app.route('/',methods=['GET','POST'])
def default():
    return "connected"


'''
on start on an RPI0 this api is called to get IPAddress and location from firebase
'''
@app.route('/rpi0/emailgetdata',methods=['POST'])
def emailgetdata():

    data = json.loads(request.get_json())
    rpidescription = data["rpidescription"]
    location = ""
    result = {}
    #if rpidescription=="sonya-cummings":
    #    location = RPI_Details["sonya-cummings"]["location"]
    #    currentIP = RPI_Details["sonya-cummings"]["IPAddress"]
    #else:
    try:
        doc_ref = db.collection("RPI-details")
        for doc in doc_ref.get():
            if doc.id == rpidescription:
                location = doc.to_dict()["location"]
                currentIP = doc.to_dict()["IPAddress"]
                break
    except:
        location = ""
        currentIP = ""
    
    result["location"] = location
    result["currentIP"] = currentIP
    
    return jsonify(result)
    
'''
    Get location of RPI0
'''   
@app.route('/rpi0/getlocation',methods=['POST'])
def getlocation():

    data = json.loads(request.get_json())
    rpidescription = data["rpidescription"]
    print(data)
    
    result = {}
    location=""
    #if rpidescription=="sonya-cummings":
    #    location = RPI_Details["sonya-cummings"]["location"]
    #else:
    try:
        doc_ref = db.collection("RPI-details")
        for doc in doc_ref.get():
            if doc.id == rpidescription:
                location = doc.to_dict()["location"]
                break
    except:
        location = ""
    
    result["location"] = location
    print(location)
    
    return jsonify(result)
    
   
'''
    If IPAddress changes to something new this api is called to update information in firebase
'''   
@app.route('/rpi0/emailsavedata',methods=['POST'])
def emailsavedata():

    data = json.loads(request.get_json())
    print(data)
    rpidescription = data["rpidescription"]
    
    result = 0
    #if rpidescription=="sonya-cummings":
    #    RPI_Details["sonya-cummings"]["IPAddress"] = data["IPAddress"]
    #    path = "/var/www/aspendb/probesearch/SensorsData/RPI-Details.json"
    #    writeJson(path, RPI_Details)
    try:
        doc_ref = db.collection("RPI-details")
        for doc in doc_ref.get():
            if doc.id == rpidescription:
                doc_ = db.collection("RPI-details").document(doc.id)
                doc_.update({"IPAddress": data["IPAddress"]})
                result = 1
                break
    except:
        pass 
    
    return jsonify(result)
    
'''
    all the sensor information are saved to firebase using this API
'''
@app.route('/rpi0/storedata',methods=['POST'])
def storedata():

    data = json.loads(request.get_json())
    storageBucket = data["rpi"]
    collectionName = data["rpi"]
    
    ''' Store Image  '''
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    
    imgRaw = data["image"]
    name = data["ImgRef"]+".jpg"
    img_decoded = base64.b64decode(imgRaw)
    imgInMem = Image.open(BytesIO(img_decoded))  
    imgInMem.save("/var/www/aspendb/probesearch/rpi0/"+name)
    
    storage.child("{}/{}".format(storageBucket,name)).put("/var/www/aspendb/probesearch/rpi0/"+name)
    os.remove("/var/www/aspendb/probesearch/rpi0/"+name)
    
    ''' Store KPI  '''
    
    docName = data["ImgRef"]
    del data["image"]
    try:
        doc_ref = db.collection(collectionName).document(docName)
        doc_ref.set(data)
        print("KPI stored")
    except Exception as err:
        print("Error: ",err)
    
    
    ##return jsonify(result)
    return ""
    
    
'''  The service runs on port 8071 '''
if __name__ == '__main__':
    #app.run(host='127.0.0.1',debug=True,port="8071")
    app.run(host='128.192.158.63', port=8072, debug=True)