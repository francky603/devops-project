FROM node:16
WORKDIR /app
COPY . /app
COPY /home/franky/voting-app/server.crt /app/server.crt
COPY /home/franky/voting-app/server.key /app/server.key
RUN npm install
CMD ["npm", "start"]
