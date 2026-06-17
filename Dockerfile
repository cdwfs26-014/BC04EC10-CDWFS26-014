FROM python:3.13
USER root
RUN mkdir /opt/app
WORKDIR /opt/app
RUN pip install flask
COPY app.py /opt/app
RUN mkdir /opt/app/templates
COPY templates /opt/app/templates/
EXPOSE 5000
ENV SLEEP_TIME="0"

USER www-data
ENTRYPOINT [ "flask", "--app", "app", "run", "--host", "0.0.0.0" ]
