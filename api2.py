import os
from datetime import datetime
import urllib.request
from flask import Flask, json, render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.json_util import dumps
# import firebase_admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



cred_obj = firebase_admin.credentials.Certificate('serviceAccountKey.jspm')
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
# app = Flask(__name__, template_folder="templates")
app =Flask(__name__)
client =  MongoClient()
print(client)
client = MongoClient(host="localhost", port=27017)
db = client.rptutorials
collection = db.tutorial


def MongodIsert(fileName,category,filePath):
    newFile={
        "FileName":fileName,
        "Category":category,
        "FilePath":filePath
    }
    result = collection.insert(newFile)
    print(" the result is",result)
    return result


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




# return json of all the images here

@app.route('/ListFiles', methods=['GET'])
def ListFile():
    cursor = list(collection.find({}))
    result=[]
    for i in cursor:
        result.append({'FileName':i['FileName'],'Category':i['Category'],'path':i['FilePath']})
    resp=jsonify({"result":result})
    return resp


# render page with images
@app.route('/getFiles',methods=['GET'])
def sendPage():
    cursor = list(collection.find({}))
    result=[]
    for i in cursor:
        result.append({'FileName':i['FileName'],'Category':i['Category'],'path':i['FilePath']})
    # resp=jsonify({"result":result})
    # return resp
    a=result
    print("/n/n/n/",a)
    rend="<ul>"
    li="<li><img src = \"static/UPLOAD_FOLDER/"
    lie="\"></li>"
    for i in result:
        rend=rend+li+i["FileName"]+lie
    rend=rend+"</ul>"
    return rend

# file uplaod post
@app.route('/file-upload', methods=['POST'])
def upload_file():
    # print("this is \n\n\n",request.files)

	# check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        now = datetime.now()
        filename = secure_filename(file.filename)
        fileName = now.strftime("%d_%m_%Y_Time_%H_%M_%S")+"."+filename.rsplit('.', 1)[1]
        print("\n\n\n",fileName)
        file.save(os.path.join('UPLOAD_FOLDER', fileName))
        response = MongodIsert(fileName=fileName,category=1,filePath="UPLOAD_FOLDER")
        print("\n\n\n entered into mongod",(str)(response))
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # UPLOAD_FOLDER
        
        resp = jsonify({'message' : 'File successfully uploaded',"Mongod":"uploaded","ObjectId":(str)(response)})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0')