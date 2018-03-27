FROM python:3-onbuild

ADD . /project1

WORKDIR /project1

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "./restAPI.py"]