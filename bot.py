import asyncio
import tomllib
from core.client import IRCClient

with open("config/config.toml", "rb") as f:
    config = tomllib.load(f)["irc"]

async def main():
    client = IRCClient(config)
    await client.connect()

asyncio.run(main())