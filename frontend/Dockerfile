FROM node:22.0.0

WORKDIR /frontend

ADD . /frontend

RUN npm install

RUN npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build"]
