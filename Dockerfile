FROM python:3.10 as python_base_online_store

ENV HOME=/home/app
ENV APP_HOME=/home/app/

RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/static

WORKDIR $APP_HOME

RUN apt-get update
RUN apt-get install -y vim redis
RUN pip install --upgrade pip
COPY ./requirements.txt $APP_HOME/requirements.txt
RUN pip install -r requirements.txt


FROM python_base_online_store

# copy project
COPY . $APP_HOME/

EXPOSE 8000

RUN redis-server --daemonize yes

RUN python manage.py makemigrations users items orders
RUN python manage.py migrate

RUN celery -A online_store worker -B --detach 
RUN nohup python manage.py runserver

# ENTRYPOINT ["/usr/local/bin/python /home/app/manage.py runserver"]
# ENTRYPOINT ["/usr/bin/nohup /usr/local/bin/python /home/app/manage.py runserver &"]
ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]