FROM python:3.12
WORKDIR /app
COPY flask-biere/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "test.py"]
