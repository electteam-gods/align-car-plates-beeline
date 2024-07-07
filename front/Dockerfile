FROM node:20 AS builder

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./

RUN npm install

COPY . ./
RUN npm run build



FROM nginx:1.17-alpine
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
CMD ["/bin/sh", "-c", "nginx -g 'daemon off;'"]

COPY --from=builder /app/dist/ /usr/share/nginx/html