FROM python:3-alpine
WORKDIR /app
COPY . /app
CMD python -m unittest discover -s tests
