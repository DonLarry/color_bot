import functools

import discord
from discord.ext import commands

from utils import allowed_member, get_hexadecimal_color, get_rgb_color, add_color_role, remove_color_role

from settings import server_id, color_role_name, reaction_emoji_id, color_role_position, colors_channel_id, allowed_users


class Bot(commands.Bot):
    # logs_channel = None

    def auth(self, func):
        @functools.wraps(func)
        async def wrapper_decorator(*args, **kwargs):
            ctx = args[0]
            if ctx.guild is None or ctx.guild.id != server_id:
                return
            if not allowed_member(ctx.author):
                # command_name = func.__name__
                # if len(args) > 1:
                #     command_name += f' {args[1]}'
                # await self.logs_channel.send(f'{ctx.author.mention} tried to use the command `{command_name}`.')
                return
            if ctx.channel.id != colors_channel_id:
                return
            value = await func(*args, **kwargs)
            return value
        return wrapper_decorator
    
    # TODO: make a decorator that receives the emoji, and react at the end if no error was raised
    # def react(self, )


def discord_bot():
    description = '''Look at my about me c:'''
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = Bot(command_prefix='color!', description=description, intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print('------')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        text = message.content.split(' ')
        text[0] = text[0].lower()
        message.content = ' '.join(text)
        await bot.process_commands(message)

    @bot.command()
    @bot.auth
    async def ping(ctx):
        print('pong')
        await ctx.send('pong')

    @bot.command()
    @bot.auth
    async def get(ctx, *args):
        usage = '''
            Usage: `color!get <color>`
             `color!get #ff0000` for hexadecimal color
             `color!get 255 0 0` for RGB color
        '''

        if len(args) != 1 and len(args) != 3:
            await ctx.send(usage)
            return

        color = None
        if len(args) == 1:
            color = get_hexadecimal_color(args[0])
        else:
            color = get_rgb_color(*args)

        # If color is None, there was an an unhandled error
        if color is None:
            await ctx.send(usage)
            return

        # If color is a string, that's a message of an error
        if type(color) is str:
            await ctx.send(color)
            return

        # Add the color role
        await add_color_role(ctx.author, color, ctx.guild)

        emoji = bot.get_emoji(reaction_emoji_id)
        await ctx.message.add_reaction(emoji)

    @bot.command()
    @bot.auth
    async def remove(ctx):
        # Remove color role
        await remove_color_role(ctx.author, ctx.guild)

        # React to the message with an emoji
        emoji = bot.get_emoji(reaction_emoji_id)
        await ctx.message.add_reaction(emoji)
    
    @bot.command()
    @bot.auth
    async def give(ctx, color, member: discord.Member):
        if ctx.author.id not in allowed_users:
            return
        usage = "Usage: `color!give <hexadecimal_color> @somone`"
        
        color = get_hexadecimal_color(color)

        # If color is None, there was an an unhandled error
        if color is None:
            await ctx.send(usage)
            return

        # If color is a string, that's a message of an error
        if type(color) is str:
            await ctx.send(color)
            return

        # Add the color role
        await add_color_role(member, color, ctx.guild)

        # React to the message with an emoji
        emoji = bot.get_emoji(reaction_emoji_id)
        await ctx.message.add_reaction(emoji)

    return bot
