FROM python:3.4.9-slim

ENV TZ=America/Sao_Paulo

RUN apt-get update -y ; \
	    apt-get install -y python-dev libsasl2-dev libldap2-dev libssl-dev mysql-client mysql-server libmariadbclient-dev gcc apt-utils tzdata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN dpkg-reconfigure -f noninteractive tzdata 

WORKDIR /opt

ADD app.py /opt/
ADD db_config.py /opt/
ADD main.py /opt/
ADD requirements.txt /opt
ADD static /opt/static
ADD templates /opt/templates

COPY docker-entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["python","/opt/main.py"]