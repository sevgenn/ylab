FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /cookbook_root
RUN pip install --upgrade pip
COPY cookbook_root/requirements.txt .
RUN pip install -r requirements.txt
COPY ./cookbook_root /cookbook_root