FROM python:3.9-slim

RUN mkdir -p /opt/app
WORKDIR /opt/app

ENV RMA_BIND_ADDRESS=0.0.0.0
ENV RMA_NUM_WOEKERS=4

COPY requirements.txt .

RUN pip install -r requirements.txt

ARG APP_PORT=80
EXPOSE $APP_PORT
ENV RMA_BIND_PORT=$APP_PORT

COPY . .

RUN chmod +x start

CMD ./start