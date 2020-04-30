FROM node:lts-alpine

LABEL description="Built on commit 4f455f44"

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build