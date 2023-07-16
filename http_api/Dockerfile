FROM python:3.10-alpine

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV RABBITMQ_URI=, INPUT_QUEUE=

EXPOSE 8000

CMD [ "uvicorn", "src:app" , "--host", "0.0.0.0", "--port", "8000"]
