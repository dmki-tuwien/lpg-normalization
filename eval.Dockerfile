FROM python:3.13-bookworm

WORKDIR /

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY run_eval.py run_eval.py
COPY normalize.py normalize.py
COPY constants.py constants.py
COPY gnfd gnfd

CMD ["python", "run_eval.py"]
