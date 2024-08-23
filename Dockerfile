FROM python:3.12-slim

WORKDIR /usr/src/app/

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "main.py"]