import requests
import sys


def send_text(text: str) -> None:
    data = {'text': text}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    r = requests.post(
        "http://0.0.0.0:8000/queue_reverse_text",
        json=data,
        headers=headers
    )
    


if __name__ == "__main__":
    sentence = sys.argv
    text = ' '.join(sentence[1:])
    send_text(text)