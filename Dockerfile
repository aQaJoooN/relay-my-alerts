FROM python:3.9-slim

ARG APP_PORT=80
EXPOSE $APP_PORT
ENV RMA_BIND_PORT=$APP_PORT

ENV RMA_BIND_ADDRESS=0.0.0.0
ENV RMA_NUM_WOEKERS=4

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . .

RUN pip install -U pip  \
   && pip install -r requirements.txt \
   && chmod +x start

CMD ./start