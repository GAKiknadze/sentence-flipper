import websocket


uri = "ws://0.0.0.0:8080/listen_results"


def on_message(ws: websocket.WebSocket, message: bytes) -> None:
    print(message.decode())


ws = websocket.WebSocketApp(
    uri,
    on_message=on_message
)

ws.run_forever()
