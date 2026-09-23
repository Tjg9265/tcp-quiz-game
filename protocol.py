"""Shared newline-delimited JSON messages for the TCP quiz game."""

import json

MAX_MESSAGE = 8192


def send_message(connection, message):
    """Encode one dictionary and send every byte, including its delimiter."""
    data = (json.dumps(message) + "\n").encode("utf-8")
    connection.sendall(data)


def receive_message(reader):
    """Read one complete message; TCP may split or combine network packets."""
    line = reader.readline(MAX_MESSAGE + 1)
    if not line:
        return None
    if len(line) > MAX_MESSAGE or not line.endswith(b"\n"):
        raise ValueError("Message is too long or incomplete.")
    message = json.loads(line.decode("utf-8"))
    if not isinstance(message, dict):
        raise ValueError("Messages must be JSON objects.")
    return message
