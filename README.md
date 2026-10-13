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

[Software Demo Video]: https://byupathwayworldwideprod-my.sharepoint.com/:v:/g/personal/tgarcia2_byupathway_edu/IQDHvIJPTFCUTafJECmrU9lCAQHG-CHSD_i7ptasGoH3sVI?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=dotLVj

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