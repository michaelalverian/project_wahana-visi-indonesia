FROM python:3.9.4
ENV PYTHONUNBUFFERED 1
WORKDIR /wvi
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt