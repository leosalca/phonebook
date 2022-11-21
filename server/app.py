from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo


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

# Format contacts
def formatContact(contact):
        return {            
            'name': contact['name'],
            'phone': contact['phone'],
            'email': contact['email'],
            'address': contact['address'],
            'company': contact['company']
        }

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/getcontacts', methods=['GET'])
def getcontacts():
    lcontacts = mongo.db.contacts.find()
    formatContactList = map(formatContact, lcontacts)
    return jsonify(list(formatContactList))

@app.route('/addcontact', methods=['POST'])
def addcontact():
    name = request.json['name']
    phone = request.json['phone']
    company = request.json['company']
    email = request.json['email']
    address = request.json['address']
    mongo.db.contacts.insert_one({'name':
    name, 'phone': phone, 'company': company, 'email': email, 'address': {'street': address['street'], 'city': address['city'], 'state': address['state'], 'zip': address['zip']}})
    print(name)
    lcontacts = mongo.db.contacts.find()
    formatContactList = map(formatContact, lcontacts)
    return jsonify(list(formatContactList))

@app.route('/deletecontact', methods=['POST'])
def deletecontact():
    name = request.json['name']
    mongo.db.contacts.delete
    lcontacts = mongo.db.contacts.find()
    formatContactList = map(formatContact, lcontacts)
    return jsonify(list(formatContactList))

@app.route('/updatecontact', methods=['POST'])
def updatecontact():
    name = request.json['name']
    phone = request.json['phone']
    company = request.json['company']
    email = request.json['email']
    address = request.json['address']
    mongo.db.contacts.update_one({'name': name}, {'$set': {'phone': phone, 'company': company, 'email': email, 'address': {'street': address['street'], 'city': address['city'], 'state': address['state'], 'zip': address['zip']}}})
    lcontacts = mongo.db.contacts.find()
    formatContactList = map(formatContact, lcontacts)
    return jsonify(list(formatContactList))

@app.route('/verifyzip', methods=['POST'])
def verifyZip():
    zip = request.json['zip']
    print(zip)
    return jsonify(zip)


if __name__ == '__main__':
    app.run()
