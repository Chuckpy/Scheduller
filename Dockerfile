FROM python:3.10.8

# set work directory
WORKDIR /backend/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements/main_requirements.txt /src/requirements/main_requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /src/requirements/main_requirements.txt
RUN rm -rf /root/.cache/pip

# Google dependencies

RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

RUN ls

CMD [ "python3", "main.py" ]