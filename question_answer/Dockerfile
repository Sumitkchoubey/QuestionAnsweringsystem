FROM python:3.6
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app/.
RUN pip install -r requirements.txt
CMD ["python","app.py"]