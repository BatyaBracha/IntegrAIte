# Build stage
FROM node:20-alpine AS build
WORKDIR /app

ARG REACT_APP_API_BASE="http://localhost:8000/api/v1"
ENV REACT_APP_API_BASE=${REACT_APP_API_BASE}

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
