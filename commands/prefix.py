import requests
from PIL import Image
import io
import os
import discord
from discord.ext import commands
import random

# Variables
about_commands = ["?about", "!about", "/about"]
help_commands = ["?help", "!help", "/help"]


################################################### bot-Command-code ########################################################


def prefix(bot):
    ############### About ########################
    @commands.command(name='about', aliases=about_commands)
    async def about(ctx):
        about = discord.Embed(
            title='About',
            description='LuminaryAI The Discord AI bot, crafted with Python and AIML, is a sophisticated conversational entity. Leveraging advanced technologies, it emulates human-like dialogue, seamlessly engaging users in natural conversations. Designed to provide a dynamic and interactive experience, this bot transforms text-based interactions into lifelike discussions within the Discord platform.',
            color=0x99ccff  # Convert hex color to integer
        )
        about.add_field(name='Owner', value="alphast101", inline=True)
        about.add_field(name='Used languages', value="Python 3.11 | AIML 0.9.2 | discord.py 2.3.2", inline=True)

        # Open the image file and resize it
        with Image.open("ai.png") as img:
            img = img.resize((400, 200))  # Adjust the size as needed

            # Save the resized image to a temporary file
            temp_filename = "resized_ai.png"
            img.save(temp_filename, "PNG")

            # Attach the resized image as a thumbnail to the embed
            about.set_image(url="attachment://resized_ai.png")

        # Send the embed without the file parameter
        await ctx.send(embed=about, file=discord.File(temp_filename, filename="resized_ai.png"))

        # Remove the temporary file after sending
        os.remove(temp_filename)

    bot.add_command(about)


    ############### Help ########################
    @commands.command(name='help', aliases=help_commands)
    async def help_command(ctx):
        help_ = discord.Embed(
            title='Help/command list',
            color=0x99ccff  # Convert hex color to integer
        )
        help_.add_field(name='?start', value="Enable AI response. Make sure you have set your AI-channel before, Otherwise the AI response don't work properly", inline=True)
        help_.add_field(name='?stop', value="Disable AI response.", inline=True)
        help_.add_field(name='?aiset {channel_id}', value="Set your AI response channel where the bot will respond.", inline=True)
        help_.add_field(name='?author', value="this command sends userID, username and user avatar.", inline=True)
        help_.add_field(name='?meme', value="this command sends a random meme. It takes a bit time", inline=True)
        help_.add_field(name='?help', value="this command sends a list of commands.", inline=True)
        help_.add_field(name='?cat', value="shows a cat.", inline=True)
        await ctx.send(embed=help_)

    bot.add_command(help_command)

    
    ####################### author #########################
    @bot.command(name='author', aliases=['!author', '/author'])
    async def author(ctx):
        user = ctx.author
        author = discord.Embed(
            title=f"User: {user}\nUserID: {user.id}",
            color=0x99ccff
        )

        # Download the image from the URL
        response = requests.get(ctx.author.avatar.url)
        response.raise_for_status()

        # Open the image from the downloaded content
        with Image.open(io.BytesIO(response.content)) as img:
            img = img.resize((300, 300))  # Adjust the size as needed

            # Save the resized image to a temporary file
            temp_filename = "resized_author_pfp.png"
            img.save(temp_filename, "PNG")

            # Attach the resized image to the embed
            file = discord.File(temp_filename, filename="resized_author_pfp.png")
            author.set_image(url="attachment://resized_author_pfp.png")

        await ctx.send(embed=author, file=file)

        # Remove the temporary file after sending
        os.remove(temp_filename)

    
    ################################ meme ######################################
    @bot.command(name="meme", aliases=['!meme', '/meme'])
    async def meme_command(ctx):
        meme_folder = "memes"
        meme_files = [file for file in os.listdir(meme_folder) if file.endswith(".png")]

        if meme_files:
            selected_photo_path = os.path.join(meme_folder, random.choice(meme_files))

            with open(selected_photo_path, "rb") as file:
                meme_send = discord.File(file)
                await ctx.reply(file=meme_send)
        else:
            await ctx.reply("An error occurred.")


    ############################# cat ########################################
    @bot.command(name="cat", aliases=['!cat', '/cat'])
    async def meme_command(ctx):
        cat_folder = "cat"
        cat_files = [file for file in os.listdir(cat_folder) if file.endswith(".png")]

        if cat_files:
            selected_photo_path = os.path.join(cat_folder, random.choice(cat_files))

            with open(selected_photo_path, "rb") as file:
                meme_send = discord.File(file)
                await ctx.reply(file=meme_send)
        else:
            await ctx.reply("An error occurred.")