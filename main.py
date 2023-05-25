from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
import os
from discord.ext import ipc

app = Quart(__name__)
ipc_client = ipc.Client(secret_key = "glitchyOnline?")

app.config["SECRET_KEY"] = os.environ['SECRET_KEY']
app.config["DISCORD_CLIENT_ID"] = 946622889317240903
app.config["DISCORD_CLIENT_SECRET"] = os.environ['CLIENT_SECRET']
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1/callback"

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
  return await render_template("home.html", authorized = await discord.authorized)


@app.route("/about")
async def about():
  return await render_template("about.html")


@app.route("/login")
async def login():
  return await discord.create_session

@app.route("/callback")
async def callback():
  try:
    await discord.callback()
  except Exception:
    pass
    
  return redirect(url_for("dashboard"))

  user = await discord.fetch_user()
  return f"{user.name}#{user.discriminator}"

@app.route("/dashboard")
async def dashboard():
  if not await discord.authorized:
    return redirect(url_for("login"))
  guild_count = await ipc_client.request("get_guild_count")
  guild_ids = await ipc_client.request("get_guild_ids")
  
  user_guilds = await discord.fetch_guilds()
  
  guilds = []
  for guild in user_guilds:
    if guild.permissions.administrator:
      guild.class_color = "green-border" if guild.id in guild_ids else "red-border"
      guilds.append(guild)

  guilds.sort(key = lambda x: x.class_color == "red-border")
  name = (await discord.fetch_user()).name
  return await render_template("dashboard.html", guild_count = guild_count, guilds = guilds, username = name)

#@app.route("/dashboard/<int:guild_id>")


if __name__ == "__main__":
  app.run(debug=True)
