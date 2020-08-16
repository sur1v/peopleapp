FROM python:3.7-alpine
LABEL maintainer="Jose Ignacio Martinez <gsuriv@gmail.com>"
EXPOSE 80/tcp
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "4", "app:app"]
