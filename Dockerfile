FROM python:3-alpine
RUN apk add --virtual .build-dependencies \ 
            --no-cache \
            python3-dev \
            build-base \
            linux-headers \
            pcre-dev

RUN apk add --no-cache pcre
WORKDIR /babymonitor
COPY . /babymonitor
RUN pip install -r requirements.txt
RUN pip install uwsgi
RUN apk del .build-dependencies && rm -rf /var/cache/apk/*
EXPOSE 5000
CMD ["uwsgi", "--ini", "/babymonitor/wsgi.ini"]