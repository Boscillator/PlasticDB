FROM python:2.7
RUN apt-get update
RUN pip install flask Flask-SQLAlchemy psycopg2
ADD ./Code /Code
RUN cat /etc/hosts
RUN python /Code/makeDB.py
CMD python /Code/debug.py