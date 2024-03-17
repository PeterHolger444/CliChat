import urwid
import socket
import threading

class ChatUI:
    def __init__(self, name):
        self.username = name
        self.chat_history = urwid.SimpleListWalker([])
        self.chat_box = urwid.ListBox(self.chat_history)
        self.input_box = urwid.Edit("> ")

        self.frame = urwid.Frame(
            body=self.chat_box,
            footer=urwid.Pile([
                urwid.Text("Enter /exit to exit"),
                self.input_box
            ])
        )

        self.wrapped_chat_box = urwid.BoxAdapter(self.chat_box, height="pack")

    def display_message(self, message):
        self.chat_history.append(urwid.Text(message))
        self.loop.draw_screen()

    def process_command(self, rawCommand):
        rawCommand = rawCommand.split(' ')
        command, args = rawCommand[0], rawCommand[1:]

        if command == "exit":
            connection.sendall( ("c,exit," + self.username).encode() )
            raise urwid.ExitMainLoop()

    def process_input(self):
        message = self.input_box.get_edit_text().strip()
        self.input_box.set_edit_text("")

        if message:
            if message[0] == '/':
                toSend = self.process_command(message[1:])

            else:
                self.display_message('[' + self.username + '] '+ message)
                toSend = ('m,' + self.username + ',' + message)
                
            try:
                connection.sendall(toSend.encode())
            except Exception as e:
                self.display_message("Error sending message: " + str(e))

    def start(self):
        self.loop = urwid.MainLoop(self.frame, unhandled_input=self.handle_input)
        self.loop.run()

    def handle_input(self, key):
        if key == "enter":
            self.process_input()

def process_receive_command(rawCommand):
    rawCommand = rawCommand[2:].split(',')
    command, args = rawCommand[0], rawCommand[1:]

    if command == "exit":
        ui.display_message('[!] User ' + args[0] + ' has existed')

def receive_messages():
    while True:
        try:
            message = connection.recv(1024).decode()
            if message:
                if message == "exit ok":
                    connection.close()
                    break

                elif message[0] == 'c':
                    process_receive_command(message)

                else:
                    username, message = message.split(',')[1:]
                    ui.display_message('[' + username + '] ' + message)
                    
        except Exception as e:
            connection.close()
            ui.display_message("Error receiving message: " + str(e))
            break

host = "127.0.0.1"
port = 9999
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((host, port))

name = input("What do you want to be called?: ")

receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

ui = ChatUI(name)
ui.start()
