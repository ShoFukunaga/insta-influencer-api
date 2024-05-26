# pull official base image
FROM python:3.12.1-slim-bookworm

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install \
    netcat-traditional \
    gcc g++ postgresql \
    build-essential \
    python3-dev \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# && python -m spacy download ja_ginza

RUN pip install -U ginza typer \
    && ginza -m ja_ginza

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

ENV PYTHONPATH /usr/src/app

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
