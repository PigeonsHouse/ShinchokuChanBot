FROM python:3.9

RUN mkdir -p /opt
WORKDIR /opt

COPY . /opt/

RUN pip install pip
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT [ "pipenv", "run", "python", "main.py" ]
