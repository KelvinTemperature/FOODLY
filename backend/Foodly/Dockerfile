FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
RUN chmod +x /app/start.sh

ENV MYSQL_HOST=host.docker.internal
ENV MYSQL_PORT=3306
ENV MYSQL_USER=Givenchi
ENV MYSQL_PASSWORD=Fauziya@123
ENV MYSQL_DATABASE=foodly_auth
ENV MONGO_URI=mongodb+srv://givenchi:Givenchi1@cluster0.2pf490a.mongodb.net/?retryWrites=true&w=majority&appName=GivenchiCodes
ENV MONGO_DB_NAME=foodly_orders
ENV JWT_SECRET_KEY=change-me-in-production

EXPOSE 5000

CMD ["/app/start.sh"]
