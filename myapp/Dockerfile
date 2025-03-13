FROM node:14

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "build"]

VOLUME ["/app/dist"]  # 让宿主机访问 `dist/`