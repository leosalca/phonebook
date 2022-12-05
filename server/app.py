from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from pymongo import MongoClient
import json as JSON
import xml.etree.ElementTree as ET
import urllib.request
from bson.objectid import ObjectId
import dns.resolver

# chnaged default dns resolver for pymongo to google's. Default for certain macs resolver was not working
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

# configuration
DEBUG = True

# instantiate the app, attach mongo URI to config. MongoDB PW needs to be in .env file
app = Flask(__name__)

# app.config['MONGO_URI'] = 'mongodb://leosalca:' + mdbPW + '@ac-fvpiouw-shard-00-00.vbmmd49.mongodb.net:27017,ac-fvpiouw-shard-00-01.vbmmd49.mongodb.net:27017,ac-fvpiouw-shard-00-02.vbmmd49.mongodb.net:27017/?ssl=true&replicaSet=atlas-zfh5kr-shard-0&authSource=admin&retryWrites=true&w=majority'
# app.config['MONGO_URI'] = 'mongodb+srv://leosalca:' + 'sagRyz-nizqu1-metzuw' + '@phonebookapp.vbmmd49.mongodb.net/phone_book?retryWrites=true&w=majority'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Load MongoDB
# mongo = PyMongo(app, app.config['MONGO_URI'])
mongo = MongoClient('mongodb+srv://leosalca:' + 'sagRyz-nizqu1-metzuw' + '@phonebookapp.vbmmd49.mongodb.net/phone_book?retryWrites=true&w=majority')
db = mongo.phone_book
contacts = db.contacts
# Checking all contacts
print('MongoDB connected')
for contact in contacts.find():
    print(contact)


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

# XML USPS root
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
    formatContactList = map(formatContact, contacts.find())
    return jsonify(list(formatContactList))

@app.route('/addcontact', methods=['POST'])
def addcontact():
    name = request.json['name']
    phone = request.json['phone']
    company = request.json['company']
    email = request.json['email']
    address = request.json['address']
    contacts.insert_one({'name':name, 'phone': phone, 'company': company, 'email': email, 'address': {'street': address['street'], 'city': address['city'], 'state': address['state'], 'zipcode': address['zipcode'], 'country': address['country']}})
    print(name)
    formatContactList = map(formatContact, contacts.find())
    return jsonify(list(formatContactList))

@app.route('/deletecontact', methods=['POST'])
def deletecontact():
    id = request.json['id']
    contacts.delete_one({'_id': ObjectId(id)})
    formatContactList = map(formatContact, contacts.find())
    return jsonify(list(formatContactList))

@app.route('/updatecontact', methods=['POST'])
def updatecontact():
    id = request.json['id']
    name = request.json['name']
    phone = request.json['phone']
    company = request.json['company']
    email = request.json['email']
    address = request.json['address']
    contacts.update_one({'_id': ObjectId(id)}, {'$set': {'name':name, 'phone': phone, 'company': company, 'email': email, 'address': {'street': address['street'], 'city': address['city'], 'state': address['state'], 'zipcode': address['zipcode'], 'country': address['country']}}})
    formatContactList = map(formatContact, contacts.find())
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
