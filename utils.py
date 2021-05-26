import discord
def choose_status_embed_color(status):
  if status == "active":
    return discord.Color.green()
  elif status == "closed":
    return discord.Color.red()
  else:
    return discord.Color.dark_gray()