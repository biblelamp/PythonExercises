import asyncio
from pyrogram import Client

api_id = 29792304
api_hash = "cbf593e29d45ede7f985b1ad057654e8"

async def main():
  async with Client("my_account", api_id, api_hash) as app:
    await app.send_message("me", "Greetings from **Pyrogram**!")

asyncio.run(main())