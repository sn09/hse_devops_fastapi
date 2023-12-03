FROM python:3.11-slim

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./main.py main.py

EXPOSE 5555

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]