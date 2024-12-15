FROM python:3.11-slim

WORKDIR /app

COPY requirments.txt /app/

RUN pip install --no-cache-dir -r requirments.txt

COPY . /app/

EXPOSE 3000

CMD ["python", "app.py"]
