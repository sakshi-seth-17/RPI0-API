from flask import Flask, jsonify,request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import requests


'''  firebase db-key  '''
cred = credentials.Certificate("/var/www/aspendb/probesearch/rpi0/db-key.json")

'''  initialize_app for firebase database '''
firebase_admin.initialize_app(cred)
db = firestore.client()



'''  initialize app for flask '''
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}},support_credentials=True)
#app.config['CORS_HEADERS'] = 'Content-Type'
    
    
'''  renders home page of the application '''
#@app.route('/firebase',methods=['GET'])
@app.route('/',methods=['GET','POST'])
def default():
    return "connected"



@app.route('/rpi0/emailgetdata',methods=['POST'])
def emailgetdata():

    data = request.get_json()
    rpidescription = data["rpidescription"]
    print(data)
    
    result = {}
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
    print(location)
    print(currentIP)
    
    return jsonify(result)
    
    
@app.route('/rpi0/emailsavedata',methods=['POST'])
def emailsavedata():

    data = request.get_json()
    print(data)
    rpidescription = data["rpidescription"]
    
    result = 0
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
    
    
'''  The service runs on port 8071 '''
if __name__ == '__main__':
    #app.run(host='127.0.0.1',debug=True,port="8071")
    app.run(host='128.192.158.63', port=8072, debug=True)