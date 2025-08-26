FROM python:3.9

RUN mkdir -p /opt
WORKDIR /opt

COPY ./Pipfile ./Pipfile.lock ./

RUN pip install pip
RUN pip install pipenv
RUN pipenv install

COPY . ./

ENTRYPOINT [ "pipenv", "run", "python", "main.py" ]
