FROM node:lts-alpine
# start from a node image. Set the working directory to /app. All subsequent commands will be run from this directory
WORKDIR /app
# copy the package.json file into the container at /app
COPY package*.json ./
# install dependencies from package.json
RUN npm install
# copy all the files from the current directory into the container at /app
COPY . .
# build the app for production
RUN npm run build
# expose port 3000 to the host
EXPOSE 3000
# run the app. This serves the app at container port :3000. Docker compose will map this to the host's port 3000
CMD [ "npm", "start" ]
