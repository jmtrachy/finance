import socket


class Bot():
    def __init__(self, name, welcome_message=''):
        self.name = name
        self.len_name = len(name)
        self.welcome_message = welcome_message
        self.simple_listeners = {}
        self.complex_listeners = {}

    def add_simple_listener(self, term, action):
        self.simple_listeners[term] = action

    def add_complex_listener(self, term, action):
        self.complex_listeners[term] = action

    def send_message(self, channel, message):
        full_message = 'PRIVMSG #' + channel + ' :' + message.rstrip() + '\r\n'
        self.send(full_message)

    def send(self, message):
        self.irc.send(message.encode())

    def connect(self, network, port, channel, password):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((network, port))

        if password is not None:
           self.irc.send(('PASS {}\n'.format(password)).encode())
        nick_command = 'NICK {}\r\n'.format(self.name)
        user_command = 'USER {} {} {} :Python IRC\r\n'.format(self.name, self.name, self.name)
        join_command = 'JOIN #{}\r\n'.format(channel)
        self.irc.send(nick_command.encode())
        self.irc.send(user_command.encode())
        self.irc.send(join_command.encode())
        self.send_message(channel, self.welcome_message)

        keep_running = True
        while keep_running:
            byte_data = self.irc.recv(1024)
            data = byte_data.decode().rstrip()
            name_index = data.find('@' + self.name)

            # Any IRC connection needs to respond with PONG when asked via a PING - otherwise the
            # IRC server will disconnect
            if data.find('PING') != -1:
                self.send('PONG ' + data.split()[1] + '\r\n')

            # If the message is not aimed at a bot simply ignore it
            elif name_index != -1:

                # Ugly string parsing nonsense to get the command and arguments
                end_name_index = name_index + self.len_name + 2
                bot_command = data[end_name_index:]
                first_space = bot_command.find(' ')
                arguments = None
                if first_space != -1:
                    arguments = bot_command[first_space + 1:]
                    bot_command = bot_command[:first_space].lower()

                # Every message will be sent to the channel - might as well initialize this up here
                message = None

                # Quit if receiving the quit command - this is universal to all bots
                if bot_command == 'quit':
                    message = self.name + ' is quitting due to popular request.  Goodbye'
                    keep_running = False
                elif bot_command == 'help':
                    message = 'I support '
                    for listener_key in self.simple_listeners.keys():
                        message += '{}, '.format(listener_key)
                    for listener_key in self.complex_listeners.keys():
                        message += '{}, '.format(listener_key)
                    message = message.strip(' ').strip(',')

                else:
                    # Send the arguments (even if still None) to the assigned listener
                    if bot_command in self.simple_listeners:
                        message = self.simple_listeners[bot_command](arguments)
                    elif bot_command in self.complex_listeners:
                        messages = self.complex_listeners[bot_command](arguments)
                        if messages is not None:
                            for m in messages:
                                self.send_message(channel, m)
                    else:
                        message = 'Command ' + bot_command + ' not found for ' + self.name

                # Send the message no matter what has been created
                if message is not None:
                    self.send_message(channel, message)