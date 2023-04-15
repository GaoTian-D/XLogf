FROM python:3.7.16

WORKDIR /usr/src/app

COPY requirements.txt ./

ENV REDIS_HOST="127.0.0.1"
ENV REDIS_PORT=6379
ENV LISTEN_DOMAIN="dns.sup0rnm4n.com"
ENV LISTEN_PORT=53

# Using douban pipy mirror
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN pip install -U pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ./init.sh
