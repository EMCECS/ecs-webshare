FROM python:3.5.2

MAINTAINER Julio Colon

RUN mkdir /src

COPY . /src

ENV SECRET_KEY mysecret

ENV EXPIRE_TIME 300

EXPOSE 5000

RUN pip3 install -r /src/requirements.txt

CMD ["python3", "/src/app.py"]
