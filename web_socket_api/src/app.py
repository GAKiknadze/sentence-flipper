import aio_pika
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK

from .config import OUTPUT_QUEUE, RABBITMQ_URI

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    app.state.rabbit_conn = await aio_pika.connect(RABBITMQ_URI)
    channel = await app.state.rabbit_conn.channel()
    app.state.queue = await channel.declare_queue(
        OUTPUT_QUEUE,
        durable=True,
    )


@app.on_event("shutdown")
async def on_shutdown():
    await app.state.rabbit_conn.close()


@app.websocket("/listen_results")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async with app.state.queue.iterator() as qiterator:
            async for message in qiterator:
                async with message.process(requeue=False):
                    await websocket.send_bytes(message.body)
    except (WebSocketDisconnect, ConnectionClosedOK):
        pass