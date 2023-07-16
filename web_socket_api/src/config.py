import os

RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://guest:guest@127.0.0.1/")

OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "output")
