FROM python:3.9
COPY main.py /app
COPY flight_db.py /app
COPY requirements.txt /app
WORKDIR /app
EXPOSE 8060
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]