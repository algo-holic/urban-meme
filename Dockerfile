FROM ibotdotout/python-opencv:latest

EXPOSE 5000

RUN mkdir -p /application

COPY requirements.txt /application/
COPY app /application/app
COPY run.py /application/

RUN pip install -r /application/requirements.txt

ENTRYPOINT python /application/run.py