FROM python:3.9-slim

EXPOSE 80

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . .

ENV RMA_BIND_ADDRESS=0.0.0.0:80
ENV RMA_NUM_WOEKERS=4

RUN pip install -U pip  \
   && pip install -r requirements.txt

CMD ./start