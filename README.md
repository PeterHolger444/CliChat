# Python CLI Chat

A simple python command line chat application using [Urwid](https://urwid.org/index.html).

### Running the chat

First, you have to install `Urwid` if you haven't. See [here](https://github.com/urwid/urwid/wiki/Installation-instructions).

Then, you can start the server.
```python
$ py server.py
```

Now, you can run the client and start chatting.
```python
$ py client.py
```

### Commands

- /exit
Exit the chat client.

### TODOS

- Let the user specify host and port number
- Encryption
- Check for already used usernames in server
- More functionalities
    - Tagging
    - File upload
    - Styling text