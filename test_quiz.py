"""Integration checks using real TCP connections on an available local port."""

import socket
import threading
import unittest

from protocol import receive_message, send_message
from server import handle_client


class QuizTests(unittest.TestCase):
    """Exercise the server over TCP instead of calling its grading methods."""

    def setUp(self):
        """Connect a client to a temporary TCP listener and start its handler."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen()
            self.client = socket.create_connection(listener.getsockname(), timeout=3)
            connection, address = listener.accept()
        self.worker = threading.Thread(target=handle_client, args=(connection, address), daemon=True)
        self.worker.start()
        self.reader = self.client.makefile("rb")

    def tearDown(self):
        """Close the client and verify its server worker exits."""
        self.reader.close()
        self.client.close()
        self.worker.join(timeout=3)
        self.assertFalse(self.worker.is_alive())

    def request(self, action, **fields):
        """Send one request and return the server's decoded response."""
        send_message(self.client, {"action": action, **fields})
        return receive_message(self.reader)

    def test_complete_quiz(self):
        """Check grading, repeated questions, duplicate answers, and completion."""
        self.assertEqual(self.request("score")["score"], 0)
        for number, answer in enumerate(["A", "B", "C", "A", "A"], 1):
            question = self.request("question")
            self.assertEqual(question["number"], number)
            self.assertNotIn("correct_answer", question)
            self.assertEqual(self.request("question"), question)
            result = self.request("answer", answer=answer)
            self.assertEqual(result["correct"], number != 5)
            self.assertEqual(self.request("answer", answer=answer)["status"], "error")
        self.assertEqual(self.request("score")["score"], 4)
        self.assertEqual(self.request("score")["answered"], 5)
        self.assertEqual(self.request("question")["status"], "finished")
        self.assertEqual(self.request("quit")["status"], "bye")
        self.assertIsNone(receive_message(self.reader))

    def test_invalid_requests(self):
        """Invalid actions and answers must not advance or score a question."""
        self.assertEqual(self.request("answer", answer="A")["status"], "error")
        self.assertEqual(self.request("unknown")["status"], "error")
        self.request("question")
        for value in [None, 3, "", "D"]:
            self.assertEqual(self.request("answer", answer=value)["status"], "error")
        self.assertEqual(self.request("score")["answered"], 0)
        self.assertTrue(self.request("answer", answer=" a ")["correct"])

    def test_split_and_combined_messages(self):
        """Message boundaries must survive multiple writes and combined requests."""
        self.client.sendall(b'{"action":')
        self.client.sendall(b'"question"}\n{"action":"score"}\n')
        self.assertEqual(receive_message(self.reader)["status"], "question")
        self.assertEqual(receive_message(self.reader)["score"], 0)

    def test_bad_json(self):
        """Malformed JSON receives an error and a clean disconnect."""
        self.client.sendall(b'not json\n')
        self.assertEqual(receive_message(self.reader)["status"], "error")
        self.assertIsNone(receive_message(self.reader))

    def test_oversized_message(self):
        """The server rejects messages exceeding its protocol limit."""
        self.client.sendall(b'x' * 8193 + b'\n')
        self.assertEqual(receive_message(self.reader)["status"], "error")

    def test_second_player_is_independent(self):
        """A second connection starts with a fresh score while the first plays."""
        self.request("question")
        self.request("answer", answer="A")
        other = QuizTests()
        other.setUp()
        try:
            self.assertEqual(other.request("score")["score"], 0)
            self.assertEqual(other.request("question")["number"], 1)
            self.assertEqual(self.request("score")["score"], 1)
        finally:
            other.tearDown()


if __name__ == "__main__":
    unittest.main()
