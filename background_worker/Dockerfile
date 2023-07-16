FROM python:3.10-alpine

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV RABBITMQ_URI=, INPUT_QUEUE=, OUTPUT_QUEUE=

CMD [ "python", "main.py"]
