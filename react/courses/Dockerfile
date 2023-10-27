# Stage 1: Build
FROM node:18 as builder
# Create app directory
WORKDIR /app
# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH
# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./
COPY package-lock.json ./
RUN npm install 
RUN npm install react-scripts -g

# add app
COPY . .
RUN npm run build --production

# Stage 2: Production nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
