import asyncio

class IRCClient:
    def __init__(self, config):
        self.server = config["server"]
        self.port = config["port"]
        self.nick = config["nick"]
        self.realname = config["realname"]
        self.password = config.get("password", "")
        self.channels = config["channels"]

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.server, self.port
        )

        if self.password:
            self.send(f"PASS {self.password}")

        self.send(f"NICK {self.nick}")
        self.send(f"USER {self.nick} 0 * :{self.realname}")

        await self.listen()

    def send(self, message):
        print(f">>> {message}")
        self.writer.write(f"{message}\r\n".encode())

    async def listen(self):
        while True:
            line = await self.reader.readline()
            if not line:
                break

            message = line.decode().strip()
            print(f"<<< {message}")

            if message.startswith("PING"):
                self.send(f"PONG {message.split()[1]}")
                continue

            if " 001 " in message: # welcome message
                for chan in self.channels:
                    self.send(f"JOIN {chan}")