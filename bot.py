import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# Flask server for health checks
app = Flask('')

@app.route('/')
def home():
    return "🤖 Minecraft IP Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# Start Flask server
keep_alive()

# Discord Bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ✅ YOUR MINECRAFT SERVER INFO
MINECRAFT_IP = "play.blendermc.fun"
MINECRAFT_PORT = "19142"

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is now online!')
    activity = discord.Game(name="Minecraft | Type 'ip'")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if 'ip' in message.content.lower():
        embed = discord.Embed(
            title="🎮 BlenderMC Server IP",
            description=f"**Server:** `{MINECRAFT_IP}`",
            color=0x00ff00
        )
        embed.add_field(name="Port", value=f"`{MINECRAFT_PORT}`", inline=True)
        embed.add_field(name="Direct Connect", value=f"`{MINECRAFT_IP}:{MINECRAFT_PORT}`", inline=False)
        await message.reply(embed=embed)
    
    await bot.process_commands(message)

@bot.command()
async def ip(ctx):
    embed = discord.Embed(
        title="🎮 BlenderMC Server Information",
        color=0x00ff00
    )
    embed.add_field(name="IP Address", value=f"`{MINECRAFT_IP}`", inline=False)
    embed.add_field(name="Port", value=f"`{MINECRAFT_PORT}`", inline=True)
    embed.add_field(name="Status", value="🟢 Online", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def server(ctx):
    await ctx.send(f"**BlenderMC Server:** `{MINECRAFT_IP}:{MINECRAFT_PORT}`")

# Run bot
token = os.environ.get('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("❌ DISCORD_TOKEN environment variable not set!")