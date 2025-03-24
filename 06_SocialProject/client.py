import socket
import threading
import cmd
import readline
import shlex

HOST = "localhost"
PORT = 1337

class CowChatClient(cmd.Cmd):
    prompt = "🐄> "

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.cow_names = []
        self.registered_cows = []
        self.listener_thread = threading.Thread(target=self.listen_server, daemon=True)
        self.listener_thread.start()
        self.update_cow_names()
    
    def listen_server(self):
        while True:
            data = self.sock.recv(1024).decode().strip()
            if not data:
                print("\nConnection closed by server.")
                break
            print(f"\n{data}")
            self.stdout.write(f"{self.prompt}{readline.get_line_buffer()}")
            self.stdout.flush()
    
    def send(self, message):
        self.sock.sendall(message.encode() + b"\n")

    def update_cow_names(self):
        self.send("cows")
        self.cow_names = self.receive_response().split(", ")
    
    def update_registered_cows(self):
        self.send("who")
        self.registered_cows = self.receive_response().split(", ")
    
    def receive_response(self):
        return self.sock.recv(1024).decode().strip()
    
    def do_who(self, arg):
        "Просмотр зарегистрированных пользователей"
        self.send("who")
    
    def do_cows(self, arg):
        "Просмотр доступных имен коров"
        self.send("cows")
    
    def do_login(self, arg):
        "login имя_коровы — зарегистрироваться под указанным именем"
        if arg in self.cow_names:
            self.send(f"login {arg}")
            self.update_registered_cows()
        else:
            print("Invalid cow name. Use 'cows' to see available names.")
    
    def do_say(self, arg):
        "say имя_коровы текст — отправить сообщение пользователю"
        parts = shlex.split(arg)
        if len(parts) < 2:
            print("Usage: say имя_коровы текст")
            return
        self.send(f"say {parts[0]} {' '.join(parts[1:])}")
    
    def do_yield(self, arg):
        "yield текст — отправить сообщение всем"
        self.send(f"yield {arg}")
    
    def do_quit(self, arg):
        "quit — отключиться"
        self.send("quit")
        self.sock.close()
        return True
    
    def complete_login(self, text, line, begidx, endidx):
        self.update_cow_names()
        return [c for c in self.cow_names if c.startswith(text)]
    
    def complete_say(self, text, line, begidx, endidx):
        self.update_registered_cows()
        return [c for c in self.registered_cows if c.startswith(text)]
    
if __name__ == "__main__":
    CowChatClient(HOST, PORT).cmdloop()

