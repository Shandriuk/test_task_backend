FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir -p website_tags

WORKDIR website_tags
COPY requirements.txt /website_tags/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . website_tags/ 
