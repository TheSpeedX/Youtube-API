FROM python:3.10.1-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./app /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
WORKDIR /code
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

