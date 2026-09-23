"""TCP quiz server. Each connected player gets an independent quiz."""

import argparse
import socket
import threading

from protocol import receive_message, send_message

# Answers stay on the server until a player submits an answer.
QUESTIONS = [
    ("What does TCP stand for?", ["Transmission Control Protocol", "Transfer Code Program", "Terminal Connection Port"], "A"),
    ("Which address refers to this computer?", ["8.8.8.8", "127.0.0.1", "1.1.1.1"], "B"),
    ("Which Python module provides network sockets?", ["random", "math", "socket"], "C"),
    ("What identifies an application endpoint on a host?", ["A port number", "A font", "A filename"], "A"),
    ("What kind of service does TCP provide?", ["Unordered messages", "A reliable ordered byte stream", "Only image transfers"], "B"),
]


class QuizSession:
    """Keep score and the pending question for one player."""

    def __init__(self):
        """Start a new player with no answers and no active question."""
        self.index = 0
        self.score = 0
        self.pending = False

    def handle(self, request):
        """Route question, answer, score, and quit requests to their responses."""
        action = request.get("action")
        if action == "question":
            return self.get_question()
        if action == "answer":
            return self.check_answer(request.get("answer"))
        if action == "score":
            return {"status": "ok", "score": self.score, "answered": self.index,
                    "total": len(QUESTIONS)}
        if action == "quit":
            return {"status": "bye", "message": "Thanks for playing!"}
        return {"status": "error", "message": "Unknown action. Use question, answer, score, or quit."}

    def get_question(self):
        """Return the pending question again until it has been answered."""
        if self.index == len(QUESTIONS):
            return {"status": "finished", "message": "Quiz complete! Check your score."}
        self.pending = True
        question, options, _ = QUESTIONS[self.index]
        return {"status": "question", "number": self.index + 1,
                "question": question, "options": options}

    def check_answer(self, answer):
        """Validate and grade one answer without allowing duplicate points."""
        if not self.pending:
            return {"status": "error", "message": "Request a question before answering."}
        if not isinstance(answer, str) or answer.strip().upper() not in ("A", "B", "C"):
            return {"status": "error", "message": "Enter A, B, or C."}
        expected = QUESTIONS[self.index][2]
        correct = answer.strip().upper() == expected
        if correct:
            self.score += 1
        self.index += 1
        self.pending = False
        return {"status": "answer", "correct": correct, "correct_answer": expected,
                "score": self.score, "answered": self.index}


def handle_client(connection, address):
    """Exchange messages until this player quits or disconnects."""
    print(f"Player connected: {address}")
    session = QuizSession()
    try:
        with connection, connection.makefile("rb") as reader:
            while True:
                try:
                    request = receive_message(reader)
                except (ValueError, UnicodeError):
                    send_message(connection, {"status": "error", "message": "Invalid message. Reconnect to play."})
                    break
                if request is None:
                    break
                response = session.handle(request)
                send_message(connection, response)
                if response["status"] == "bye":
                    break
    except OSError as error:
        print(f"Connection ended: {error}")
    finally:
        print(f"Player disconnected: {address}")


def serve(host, port):
    """Listen for TCP connections and give each client its own worker thread."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind((host, port))
        listener.listen()
        print(f"Quiz server listening on {host}:{port}. Press Ctrl+C to stop.")
        while True:
            connection, address = listener.accept()
            worker = threading.Thread(target=handle_client, args=(connection, address), daemon=True)
            worker.start()


def main():
    """Read optional network settings and start the server."""
    parser = argparse.ArgumentParser(description="Run the TCP quiz server.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    try:
        serve(args.host, args.port)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as error:
        print(f"Could not run server: {error}")


if __name__ == "__main__":
    main()
