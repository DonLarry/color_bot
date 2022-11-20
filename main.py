import os

from discord_bot import discord_bot

from settings import DEBUG


if __name__ == '__main__':
    bot = discord_bot()
    env_identifier = 'DISCORD_BOT_TOKEN_TEST' if DEBUG else 'DISCORD_BOT_TOKEN'
    # env_identifier = 'DISCORD_BOT_TOKEN'
    bot.run(os.getenv(env_identifier))
