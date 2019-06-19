FROM python:3.7-slim
MAINTAINER Hotels.com Technology CRT Cloud <HcomTechCRTC-DebrecenDev@expedia.com>

ENV PYTHONUNBUFFERED 1

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install build-essential \
	&& apt-get -y install python3 \
	&& apt-get -y install python3-dev

COPY ./app /app
WORKDIR /app
	
RUN pip3 install --no-cache-dir numpy
RUN pip3 install --no-cache-dir -r requirements.txt

COPY nginx.conf /etc/nginx

RUN chmod +x ./start.sh

CMD ["./start.sh"]