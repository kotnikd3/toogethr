FROM node:lts-alpine
RUN npm install -g http-server
# make the 'frontend' folder the current working directory
WORKDIR /frontend
# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./
# install project dependencies
RUN npm install
# copy project files and folders to the current working directory (i.e. 'frontend' folder)
COPY . .
# build app for production with minification
RUN npm run build


EXPOSE 8080
CMD [ "http-server", "--proxy", "http://localhost:8080?", "dist" ]