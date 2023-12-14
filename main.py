import discord
from discord.ext import commands
from discord import app_commands
from aiml import Kernel
import os
import io
import requests
import random
###############################
from commands.prefix import *
from commands.prefix import prefix
from commands.slash import slash

intents = discord.Intents.all()
activity = discord.Game(name="?help")
bot = commands.Bot(command_prefix="?", intents=intents, activity=activity, status=discord.Status.do_not_disturb, help_command=None)
prefix(bot)
slash(bot)

aiml_folder = "D:/.vscode/Discord bot code test/data"

# Dictionary to store server-specific data
server_data = {}
ai_channels = {}

class SimpleChatbot:
    def __init__(self):
        self.kernel = Kernel()

        # Load AIML files from the specified folder
        for file in os.listdir(aiml_folder):
            if file.endswith(".aiml"):
                aiml_file = os.path.join(aiml_folder, file)
                self.kernel.learn(aiml_file)

    def get_response(self, user_input):
        response = self.kernel.respond(user_input)
        return response

# Create an instance of SimpleChatbot
chatbot = SimpleChatbot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.tree.sync()

async def set_ai_channel(message):
    try:
        channel_id = int(message.content.split(' ')[1])
        ai_channels[message.guild.id] = channel_id
        await message.channel.send(f'AI channel set to {channel_id} for this server')
    except ValueError:
        await message.channel.send('Invalid channel ID.')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user or message.author.bot:
        return

    # Get or create server-specific data
    server_id = message.guild.id
    if server_id not in server_data:
        server_data[server_id] = {'response_enabled': False}

    ######################### AI-enable-or-disable ##########################

    # Check for command to start/stop responses
    if message.content.lower() == "?start":
        # Check if the user is a moderator, administrator, or has a specific role
        if any(role.permissions.manage_messages for role in message.author.roles) or message.author.id == 1026388699203772477:  # Replace with your user ID
            server_data[server_id]['response_enabled'] = True
            await message.channel.send("AI enabled.")
        else:
            await message.channel.send("You don't have permission to use this command.")

    elif message.content.lower() == "?stop":
        # Check if the user is a moderator, administrator, or has a specific role
        if any(role.permissions.manage_messages for role in message.author.roles) or message.author.id == 1026388699203772477:  # Replace with your user ID
            server_data[server_id]['response_enabled'] = False
            await message.channel.send("AI disabled.")
        else:
            await message.channel.send("You don't have permission to use this command.")

    ####################### AI-Response-using-AIML ######################

    # Check if responses are enabled for the server
    if message.content.startswith('?aiset'):
        await set_ai_channel(message)
    elif server_data[server_id]['response_enabled'] and server_id in ai_channels and message.channel.id == ai_channels[server_id]:
        # Process AIML response using the chatbot instance
        response = chatbot.get_response(message.content)

        # Send the response to the same channel
        await message.channel.send(response)
    else:
        await bot.process_commands(message)

bot.run("MTE3NzY2MzcxMzE1MTU1MzYzOA.Gi40kn.ksoxXL7RrWck4-ZY_UJxb_vSSrNmO5X3rKKkJ4")