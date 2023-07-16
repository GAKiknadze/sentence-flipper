from functools import partial
from typing import Annotated
from pydantic import BaseModel, Field
import aio_pika
from fastapi import Body, FastAPI

from .config import INPUT_QUEUE, RABBITMQ_URI

app = FastAPI()

new_message = partial(aio_pika.Message, delivery_mode=aio_pika.DeliveryMode.PERSISTENT)


@app.on_event("startup")
async def on_startup():
    app.state.rabbit_conn = await aio_pika.connect(RABBITMQ_URI)


@app.on_event("shutdown")
async def on_shutdown():
    await app.state.rabbit_conn.close()


class Data(BaseModel):
    text: str


@app.post("/queue_reverse_text", status_code=201)
async def queue_reverse_text(data: Annotated[Data, Body()]):
    async with app.state.rabbit_conn.channel() as channel:
        await channel.default_exchange.publish(
            new_message(data.text.encode()), routing_key=INPUT_QUEUE
        )
    return
