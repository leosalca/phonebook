from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import json as JSON
import xml.etree.ElementTree as ET
import urllib.request
from bson.objectid import ObjectId

# configuration
DEBUG = True

# instantiate the app, attach mongo URI to config. MongoDB PW needs to be in .env file
mdbPW = 'sagRyz-nizqu1-metzuw'
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://leosalca:' + mdbPW + '@phonebookapp.vbmmd49.mongodb.net/phone_book?retryWrites=true&w=majority'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Load MongoDB
mongo = PyMongo(app)

# Format contacts function used in multiple routes
def formatContact(contact):
        return {
            'id': str(contact['_id']),
            'name': contact['name'],
            'phone': contact['phone'],
            'email': contact['email'],
            'address': contact['address'],
            'company': contact['company']
        }

#XML USPS root
uspsRoot = ET.Element('CityStateLookupRequest', {'USERID': '249LSCDE3365'})
zipXML = ET.SubElement(uspsRoot, 'ZipCode')
zip5 = ET.SubElement(zipXML, 'Zip5')
zipTree = ET.ElementTree(uspsRoot)


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
    mongo.db.contacts.insert_one({'name':name, 'phone': phone, 'company': company, 'email': email, 'address': {'street': address['street'], 'city': address['city'], 'state': address['state'], 'zipcode': address['zipcode'], 'country': address['country']}})
    print(name)
    lcontacts = mongo.db.contacts.find()
    formatContactList = map(formatContact, lcontacts)
    return jsonify(list(formatContactList))

@app.route('/deletecontact', methods=['POST'])
def deletecontact():
    id = request.json['id']
    mongo.db.contacts.delete_one({'_id': ObjectId(id)})
    lcontacts = mongo.db.contacts.find()
    formatContactList = map(formatContact, lcontacts)
    return jsonify(list(formatContactList))

@app.route('/updatecontact', methods=['POST'])
def updatecontact():
    id = request.json['id']
    name = request.json['name']
    phone = request.json['phone']
    company = request.json['company']
    email = request.json['email']
    address = request.json['address']
    mongo.db.contacts.update_one({'_id': ObjectId(id)}, {'$set': {'name':name, 'phone': phone, 'company': company, 'email': email, 'address': {'street': address['street'], 'city': address['city'], 'state': address['state'], 'zipcode': address['zipcode'], 'country': address['country']}}})
    lcontacts = mongo.db.contacts.find()
    formatContactList = map(formatContact, lcontacts)
    return jsonify(list(formatContactList))

@app.route('/verifyzip', methods=['POST'])
def verifyzip():
    zip = request.json['zip']
    zip5.text = zip
    # verify xml in console
    ET.dump(zipTree)
    # parse XML data to URL string
    docString = urllib.parse.quote(ET.tostring(zipTree.getroot()))
   
    #request to USPS
    with urllib.request.urlopen('http://production.shippingapis.com/ShippingAPI.dll?API=CityStateLookup&XML=' + docString) as response:
        xmlData = response.read()
        print(xmlData)
        root = ET.fromstring(xmlData)
        if response.status == 200:
            for address in root.findall('ZipCode'):
                if address.find('Error') is None:
                    return jsonify({'city': address.find('City').text, 'state': address.find('State').text})
                else:
                    #extract error message
                    return jsonify({'error': address.findall('Error')[0].find('Description').text})
                    
        else:
            return jsonify({'error': 'Invalid Zip Code'})


if __name__ == '__main__':
    app.run()
