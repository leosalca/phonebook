from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import xml.etree.ElementTree as ET
import urllib.request
from bson.objectid import ObjectId
import dns.resolver

# chnaged default dns resolver for pymongo to google's. Default for certain macs resolver was not working
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

# configuration
DEBUG = True

# Load .env file in root directory
load_dotenv()

# instantiate the app, attach mongo URI to config. MongoDB PW needs to be in .env file
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Load MongoDB
mongo = MongoClient('mongodb+srv://' + os.getenv('MONGODB_USER') + ':' + os.getenv('MONGODB_PW') + '@phonebookapp.vbmmd49.mongodb.net/phone_book?retryWrites=true&w=majority')
db = mongo.phone_book
contacts = db.contacts
# Checking all contacts
print('MongoDB Contacts:')
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

def formatRequestJSON(request):
    return {
        'name': request.json['name'],
        'phone': request.json['phone'],
        'email': request.json['email'],
        'address': request.json['address'],
        'company': request.json['company']
    }

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/getcontacts', methods=['GET'])
def getContacts():
    formatContactList = map(formatContact, contacts.find())
    return jsonify(list(formatContactList))

@app.route('/addcontact', methods=['POST'])
def addContact():
    reqContact = formatRequestJSON(request)
    contacts.insert_one(reqContact)
    formattedContactList = map(formatContact, contacts.find())
    return jsonify(list(formattedContactList))

@app.route('/deletecontact', methods=['POST'])
def deleteContact():
    contactobjId = request.json['id']
    contacts.delete_one({'_id': ObjectId(contactobjId)})
    formatContactList = map(formatContact, contacts.find())
    return jsonify(list(formatContactList))

@app.route('/updatecontact', methods=['POST'])
def updateContact():
    # get contact object id from request, to be used in update query
    contactobjId = request.json['id']
    # format form data MongoDB object
    reqContact = formatRequestJSON(request)
    # update MongoDB contact using 'contacts' collection
    contacts.update_one({'_id': ObjectId(contactobjId)}, {'$set': reqContact})
    formatContactList = map(formatContact, contacts.find())
    return jsonify(list(formatContactList))

@app.route('/verifyzip', methods=['POST'])
def verifyZip():
    # XML USPS root
    uspsRoot = ET.Element('CityStateLookupRequest', {'USERID': os.getenv('USPS_USERID')})
    # XML USPS child
    zipXML = ET.SubElement(uspsRoot, 'ZipCode')
    # XML USPS child where zip code from request is inserted
    zip5 = ET.SubElement(zipXML, 'Zip5')
    # create XML tree
    zipTree = ET.ElementTree(uspsRoot)
    # get zip code from request
    zip = request.json['zip']
    # insert zip code into XML
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
