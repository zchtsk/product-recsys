FROM node:16
WORKDIR /app
COPY client/package.json client/package-lock.json ./
RUN npm install -g npm@9.1.2
RUN npm ci
COPY client .
RUN npm run build
ENV PORT 3000
ENV VITE_API_CLIENT $VITE_API_CLIENT
EXPOSE 3000
EXPOSE 24678
CMD ["node", "build"]