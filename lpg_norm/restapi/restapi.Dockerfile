FROM python:3.13-bookworm

RUN mkdir /app

WORKDIR /app

RUN pip install --upgrade pip

COPY restapi/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY normalize.py lpg_norm/normalize.py
COPY logger.py lpg_norm/logger.py
COPY gofd lpg_norm/gofd
COPY restapi restapi

CMD ["fastapi", "run", "restapi/restapi.py"]
