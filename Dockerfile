FROM python:3.9-slim

EXPOSE 8080

RUN mkdir -p /opt/app \
    && useradd -M -d /opt/app relayAlerts
WORKDIR /opt/app

ENV RMA_BIND_ADDRESS=0.0.0.0
ENV RMA_NUM_WOEKERS=4

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x start

USER relayAlerts:relayAlerts

CMD ./start