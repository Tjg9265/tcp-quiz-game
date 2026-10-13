# Overview

I built a quiz game in Python where a client connects to a server
to answer networking questions.

To run the game, open two terminals in the project folder.
Start the server in the first terminal:

```text
python server.py
```

Then start the client in the second terminal:

```text
python client.py
```

[Software Demo Video](REPLACE_WITH_YOUR_YOUTUBE_LINK)

# Network Communication

The game uses a client/server setup.
Both programs use TCP and default to port 5000.

# Development Environment

I used Visual Studio Code to write the program and two terminals
to run and test it.

# Useful Websites

* [Python socket documentation](https://docs.python.org/3/library/socket.html)
* [Python JSON documentation](https://docs.python.org/3/library/json.html)

# Future Work

* Add more questions and let players choose a category.
* Mix up the question order.
* Save scores between games.