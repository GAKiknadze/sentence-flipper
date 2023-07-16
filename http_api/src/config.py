import os

RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://guest:guest@127.0.0.1/")

INPUT_QUEUE = os.getenv("INPUT_QUEUE", "input")
