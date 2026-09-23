# TCP Quiz Game

## Overview

A Python networking project with a separate TCP server and interactive client.
Players request questions, submit answers, and check their scores. The server
stores the correct answers and maintains a separate score for each connection.
Five multiple-choice networking questions are included.

This project supports learning about sockets, TCP, request/response messages,
JSON, and connection handling. Review and customize the code as you learn it.

Video demonstration: add your recorded video link to the submission document.
Including that link here is optional under the supplied submission instructions.

## Run the game

Install Python 3.10 or newer. No third-party packages are required.
Open two terminals in this folder. In the first run:

```text
python server.py
```

In the second run:

```text
python client.py
```

Choose 1 to request a question, 2 to submit A/B/C, 3 to check your score,
or 4 to disconnect. Requesting the same unanswered question does not skip it.
After all five questions, check the final score. Reconnect to start a new game.
Stop the server with Ctrl+C. Additional clients can play independently.

For two computers on a trusted local network, run the server with
`python server.py --host 0.0.0.0`, then run the client with
`python client.py --host SERVER_LOCAL_IP`. Replace SERVER_LOCAL_IP with the
server computer's actual local IPv4 address. Allow the server through the
local firewall if prompted. Both programs accept `--port 5000` to choose a port.
The default address, 127.0.0.1, connects only on the same computer.

## Network protocol

TCP carries bytes, not separate JSON messages. Each UTF-8 JSON object ends in a
newline; a buffered reader collects one whole line even when packets split or
combine messages. `sendall` sends the complete encoded message.

| Request | Example | Response |
| --- | --- | --- |
| Question | `{"action":"question"}` | Question number, text, options |
| Answer | `{"action":"answer","answer":"A"}` | Correctness, correct answer, score |
| Score | `{"action":"score"}` | Score, answered count, total |
| Quit | `{"action":"quit"}` | Goodbye message, then disconnect |

Invalid answers do not consume a question. Answers without a pending question
are rejected. Unknown actions return errors. Malformed or oversized messages
receive an error and the connection closes. Scores are held in memory and
reset on reconnect. This learning project has no accounts or encryption.

## Code walkthrough

- `server.py`: question bank, player state, grading, TCP listener, client threads.
- `client.py`: menu, connection, requests, and readable responses.
- `protocol.py`: shared JSON encoding and message framing.
- `test_quiz.py`: automated tests using real local TCP connections.

Follow one request from `build_request` through `send_message`,
`receive_message`, `QuizSession.handle`, and back to `display_response`.
Notice that grading occurs on the server and each client gets a new session.

## Development Environment

Python 3 and its standard library: socket, threading, argparse, json, unittest.

## Useful Websites

- [Python socket documentation](https://docs.python.org/3/library/socket.html)
- [Python JSON documentation](https://docs.python.org/3/library/json.html)

## Future Work

- Add question categories and randomized question order.
- Save scores between sessions.
- Add a graphical client.

## Course completion notes

This README is a project draft; compare its sections with the official
Networking README template before submitting, since that template could not
be retrieved. Add your own learning reflections where required. Record actual
hours, create the required face/demo/code video, publish your repository, and
post the video in the appropriate Teams channel. These steps are not completed
by generating the code.
