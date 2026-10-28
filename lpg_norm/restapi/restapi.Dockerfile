FROM python:3.13-bookworm

RUN mkdir /app

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY normalize.py normalize.py
COPY gofd gofd
COPY restapi restapi

CMD ["fastapi", "run", "restapi/restapi.py"]
