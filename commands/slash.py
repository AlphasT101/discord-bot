import discord
from discord import app_commands
import os
import random
from PIL import Image
import io
import requests

def slash(bot):

    ##### check #######
    @bot.tree.command(name="status", description="Check bot status")
    async def check(interaction: discord.Interaction):
        await interaction.response.send_message("bot is online")

    ##### help #######
    @bot.tree.command(name="help", description="Help/command list")
    async def help(interaction: discord.Interaction):
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

        await interaction.response.send_message(embed=help_)


    ############### about ##################
    @bot.tree.command(name="about", description="about the bot")
    async def about(interaction: discord.integrations):
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
        await interaction.response.send_message(embed=about, file=discord.File(temp_filename, filename="resized_ai.png"))

        # Remove the temporary file after sending
        os.remove(temp_filename)

    ################# author ##################
    @bot.tree.command(name="author", description="Sends user information")
    async def about(interaction: discord.Interaction):
        await interaction.response.send_message("The process cannot access user.avatar because it is being used by another process. Please try using `?author`", delete_after=5)



    ################ meme ###################
    @bot.tree.command(name="meme", description="posts a random meme.")
    async def meme(interaction: discord.Interaction):
        meme_folder = "memes"
        meme_files = [file for file in os.listdir(meme_folder) if file.endswith(".png")]
        meme_embed = discord.Embed(title="LuminaryAI - meme", description="Here is your meme", color=0x99ccff)
        try:
            if meme_files:
                selected_photo_path = os.path.join(meme_folder, random.choice(meme_files))

                with open(selected_photo_path, "rb") as file:
                    meme_send = discord.File(file)
                    await interaction.response.send_message(embed=meme_embed, file=meme_send)
            else:
                await interaction.response.send_message("An error occurred.")
        
        except discord.errors.NotFound as e:
            # Log the error, and optionally handle it appropriately
            print(f"Error sending follow-up message: {e}")
            interaction.followup.send(f"Error sending follow-up message: {e}. /n Please try using `?meme`")


    ##################### cat #######################
    @bot.tree.command(name="cat", description="shows a cat")
    async def cat(interaction: discord.Interaction):
            cat_folder = "cat"
            cat_files = [file for file in os.listdir(cat_folder) if file.endswith(".png")]

            if cat_files:
                selected_photo_path = os.path.join(cat_folder, random.choice(cat_files))

                with open(selected_photo_path, "rb") as file:
                    meme_send = discord.File(file)
                    await interaction.followup.send(file=meme_send)
            else:
                await interaction.followup.send("An error occurred.")