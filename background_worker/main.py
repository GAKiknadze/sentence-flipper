import asyncio
import os
from functools import partial
from loguru import logger
import aio_pika

RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://guest:guest@127.0.0.1/")
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "input")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "output")

new_message = partial(aio_pika.Message, delivery_mode=aio_pika.DeliveryMode.PERSISTENT)


async def main() -> None:
    connection = await aio_pika.connect(RABBITMQ_URI)
    logger.info("Worker was started")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(
            INPUT_QUEUE,
            durable=True,
        )
        
        await channel.declare_queue(
            OUTPUT_QUEUE,
            durable=True
        )
        
        exchange = channel.default_exchange

        async with queue.iterator() as qiterator:
            async for message in qiterator:
                async with message.process(requeue=False):
                    original = message.body.decode()
                    reverse = original[::-1]
                    body = f"input: {original}, output: {reverse}"
                    logger.info(body)
                    await exchange.publish(
                        new_message(body.encode()), routing_key=OUTPUT_QUEUE
                    )


if __name__ == "__main__":
    asyncio.run(main())
