FROM python:3
ADD . .
WORKDIR .
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
