from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from requests import request

# configuration
DEBUG = True

# instantiate the app, attach mongo
# MongoDB PW
mdbPW = 'sagRyz-nizqu1-metzuw'
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://leosalca:' + mdbPW + '@phonebookapp.vbmmd49.mongodb.net/phone_book?retryWrites=true&w=majority'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Load MongoDB
mongo = PyMongo(app)



# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/getcontacts', methods=['GET'])
def getcontacts():
    lcontacts = mongo.db.contacts.find()
    for contact in lcontacts:
        print(contact)
        output = [
            {
                'name' : contact['name'],
                'phone' : contact['phone'],
                'company' : contact['company'],
                'email' : contact['email'],
                'address' : contact['address']
            } 
            for contact in lcontacts]
        return jsonify(output)

@app.route('/addcontact', methods=['POST'])
def addcontact():
    raw_data = request.get_json()
    print(raw_data)


if __name__ == '__main__':
    app.run()
