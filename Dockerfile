FROM node:20-alpine

WORKDIR /app

COPY package_updated.json ./package.json

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]


