FROM ibotdotout/python-opencv:latest

RUN apt-get -y --fix-missing update
RUN apt-get -y --fix-missing install tesseract-ocr libtesseract-dev libleptonica-dev build-essential
RUN pip install Cython
RUN pip install tesserocr
RUN pip install Flask==0.11.1

EXPOSE 5000

RUN mkdir -p /application

COPY requirements.txt /application/
COPY app /application/app
COPY run.py /application/

RUN pip install -r /application/requirements.txt

ENTRYPOINT python /application/run.py