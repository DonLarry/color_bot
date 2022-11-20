import os

from dotenv import load_dotenv


load_dotenv()


DEBUG = True

server_id = int(os.getenv('SERVER_ID'))
color_role_name = '✿'
reaction_emoji_id = int(os.getenv('REACTION_EMOJI_ID'))
owner_id = int(os.getenv('OWNER_ID'))
developer_id = int(os.getenv('DEVELOPER_ID')),
allowed_users = {
    owner_id,
    developer_id,
}
allowed_roles = {
    int(os.getenv('ALLOWED_ROLE_1_ID')),
    int(os.getenv('ALLOWED_ROLE_2_ID')),
    int(os.getenv('ALLOWED_ROLE_3_ID')),
}
color_role_position = int(os.getenv('COLOR_ROLE_POSITION'))
colors_channel_id = int(os.getenv('COLORS_CHANNEL_ID'))

if DEBUG:
    server_id = int(os.getenv('DEBUG_SERVER_ID'))
    color_role_name = '✿'
    reaction_emoji_id = int(os.getenv('DEBUG_REACTION_EMOJI_ID'))
    allowed_users = {
        int(os.getenv('DEVELOPER_ID')),
    }
    allowed_roles = {
        int(os.getenv('DEBUG_ALLOWED_ROLE_1_ID')),
    }
    color_role_position = int(os.getenv('DEBUG_COLOR_ROLE_POSITION'))
    colors_channel_id = int(os.getenv('DEBUG_COLORS_CHANNEL_ID'))
