import discord
from replit import db
global NOTIFICATIONS

if "notifications" in db.keys():
  NOTIFICATIONS = db["notifications"]
else:
  NOTIFICATIONS = db["notifications"] = []

def choose_status_embed_color(status):
  if status == "active":
    return discord.Color.green()
  elif status == "closed":
    return discord.Color.red()
  else:
    return discord.Color.dark_gray()

def add_notification(data):
  global NOTIFICATIONS
  NOTIFICATIONS.insert(0, data)
  db["notifications"] = NOTIFICATIONS[:10]
  return NOTIFICATIONS