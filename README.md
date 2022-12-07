# Leo's Phonebook App
## A Vue-Flask-MongoDB Phonebook type Project
Built with a **Vue** front-end and a **Flask** back-end. Integrated with USPS Web Tools API to validate zipcodes

## Front-end tech:
- JavaScript
- TypeScript
- Vue.js
  - Pinia
  - Vuelidate
  - Naive UI Components
- Node.js

## Back-end tech:
- Python
- Flask
- MongoDB
- Docker (Desktop, hub)

## Requirements:
1. Download [Docker](https://docs.docker.com/desktop/) desktop for your system and login to your [Docker](https://hub.docker.com) hub account.


## To run the app:
1. Clone the repo, then navigate to the root directory */phonebook*.
> *cd phonebook*
2. Make sure an .env file is present with the following variables:
```
MONGODB_USER = ''
MONGODB_PW = ''
USPS_USERID = ''
```
then, use 
```
docker compose up
```
to *build* and *containerize* the phonebook app.

3. If successful, navigate to the front-end, *http://localhost:3000*, and interact with the app!
