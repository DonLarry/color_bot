import os, sys

from discord import Color, Member, Guild, Emoji

import requests

from config import allowed_users, allowed_roles, color_role_name, color_role_position


def _allowed_role(member):
    for role in member.roles:
        if role.id in allowed_roles:
            return True
    return False


def allowed_member(member):
    return member.id in allowed_users or _allowed_role(member)


def get_hexadecimal_color(color):
    if color.startswith('#'):
        color = color[1:]
    else:
        return 'Hexadecimal color should start with a `#`'
    if len(color) != 6:
        return 'Hexadecimal color must have a length of 6 characters'
    if color == '000000':
        return 'Sorry, the Hexadecimal 000000 color is reserved for transparent roles.\nHint: try using another like 000001'
    try:
        return Color(int(color, 16))
    except Exception as e:
        print(f'Exception on get_hexadecimal_color: {e}', file=sys.stderr)
        return None


def _valid_rgb_color(c):
    return 0 <= c <= 255


def _valid_rgb_colors(r, g, b):
    return _valid_rgb_color(r) and _valid_rgb_color(g) and _valid_rgb_color(b)


def get_rgb_color(r, g, b):
    try:
        r = int(r)
        g = int(g)
        b = int(b)
        
        if not _valid_rgb_colors(r, g, b):
            return 'RGB colors must have a value between 0 and 255'
        
        if r + g + b == 0:
            return 'Sorry, the RGB 0 0 0 color is reserved for transparent roles.\nHint: try using another like 0 0 1'

        return Color.from_rgb(r, g, b)
    except Exception as e:
        print(f'Exception on get_rgb_color: {e}', file=sys.stderr)
        return None


def _get_color_roles(roles):
    return [role for role in roles if role.name == color_role_name]


def _get_non_used_color_roles(roles):
    return [role for role in roles if role.name == color_role_name and len(role.members) == 0]


async def remove_color_role(member: Member, guild: Guild):
    # Remove the old roles from the member
    old_roles = _get_color_roles(member.roles)
    if old_roles:
        await member.remove_roles(*old_roles)

    # Remove the non-used color roles
    for role in _get_non_used_color_roles(guild.roles):
        await role.delete()


async def add_color_role(member: Member, color: Color, guild: Guild):
    # Remove color role
    await remove_color_role(member, guild)

    # Create the new role
    new_role = await guild.create_role(name=color_role_name, color=color)

    # Add the new role to the member
    await member.add_roles(new_role)

    # Move the new role position
    await guild.edit_role_positions({new_role: len(guild.roles)-color_role_position})


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()
    import code
    code.interact(local=locals())
