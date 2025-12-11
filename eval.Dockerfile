FROM python:3.13-bookworm

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY run_eval.py run_eval.py
COPY slpgd slpgd

CMD ["python", "run_eval.py"]
