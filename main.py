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
  except:
    return redirect(url_for("login"))

  user = await discord.fetch_user()
  return f"{user.name}#{user.discriminator}"

@app.route("/dashboard")
async def dashboard():
  guild_count = await ipc_client.request("get_guild_count")
  guild_ids = await ipc_client.request("get_guild_ids")
  user_guilds = await discord.fetch_guilds()
  same_guilds = []
  for guild in user_guilds:
    if guild.id in guild_ids:
      same_guilds.append(guild)
  return await render_template("dashboard.html", guild_count = guild_count, matching = same_guilds[0].name)

if __name__ == "__main__":
  app.run(debug=True)
