FROM python:latest

COPY sentiment-app.py requirements.txt ./

RUN pip install -r requirements.txt

CMD [ "python", "./sentiment-app.py" ]
