import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

activity = discord.Activity(type=discord.ActivityType.watching, name="Avatars")
bot = commands.Bot(command_prefix="!", activity=activity)

@bot.event
async def on_ready() -> None:
    print(
        f"Bot is ready, invite link: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot\n\n"
    )

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return

    if message.content == "hello":
        await message.channel.send("hi")

    await bot.process_commands(message)

cogs_list = [
    "misc",
    "psn",
    "psprices"
]

if __name__ == "__main__":
    for cog in cogs_list:
        print(f"Loading cog: {cog}...")
        bot.load_extension(f"cogs.{cog}")
        print(f"Loaded cog: {cog}.")
    
    print("\nStarting bot...")
    bot.run(os.getenv("TOKEN"))