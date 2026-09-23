"""Interactive menu for the TCP quiz game."""

import argparse
import socket

from protocol import receive_message, send_message


def build_request(choice):
    """Translate a menu selection into a request for the server."""
    if choice == "1":
        return {"action": "question"}
    if choice == "2":
        return {"action": "answer", "answer": input("Your answer (A/B/C): ").strip()}
    if choice == "3":
        return {"action": "score"}
    if choice == "4":
        return {"action": "quit"}
    return None


def display_response(response):
    """Display question options, grading feedback, scores, or server messages."""
    status = response.get("status")
    if status == "question":
        print(f"\nQuestion {response['number']}: {response['question']}")
        for letter, option in zip("ABC", response["options"]):
            print(f"  {letter}. {option}")
    elif status == "answer":
        if response["correct"]:
            print("Correct!")
        else:
            print(f"Incorrect. The correct answer was {response['correct_answer']}.")
        print(f"Score: {response['score']} / {response['answered']} answered")
    elif "total" in response:
        print(f"Score: {response['score']} / {response['answered']} answered; {response['total']} questions total")
    else:
        print(response.get("message", "Unexpected response."))


def play(host, port):
    """Keep one TCP connection open for the player's entire quiz session."""
    with socket.create_connection((host, port), timeout=10) as connection:
        with connection.makefile("rb") as reader:
            print("Connected to the quiz server!")
            while True:
                print("\n1. Get question\n2. Submit answer\n3. Check score\n4. Quit")
                request = build_request(input("Choose 1-4: ").strip())
                if request is None:
                    print("Please choose 1, 2, 3, or 4.")
                    continue
                send_message(connection, request)
                response = receive_message(reader)
                if response is None:
                    print("The server closed the connection.")
                    break
                display_response(response)
                if response.get("status") == "bye":
                    break


def main():
    """Read the server address and report connection failures clearly."""
    parser = argparse.ArgumentParser(description="Play the TCP quiz game.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    try:
        play(args.host, args.port)
    except (OSError, ValueError, UnicodeError) as error:
        print(f"Connection error: {error}. Check that the server is running and the address is correct.")
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
