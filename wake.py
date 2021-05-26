from flask import Flask
from threading import Thread
from replit import db
#import discord
#from .main import client
#
app = Flask('')


@app.route('/')
def home():
	return "Hello. I am alive!"


# @app.route('/bets')
# def view_bets():
#     db_value = ''
#     return """
#     <h1>{}</h1>
#     <p></p>
#     <input onclick="add_something"/>
#     """.format("match_name", "odds1", "odds2")

# def add_something():
#   client
#   pass

#app2 = Flask('')


def run():
	app.run(host='0.0.0.0', port=8080)


def wake():
	try:
		idx+= 1
	except:
		idx = 1
	if idx == 6 * 24:
		for user in db.keys():
			if db[user] < 500:
				db[user] += 25
        #print("25")
				idx = 1
	t = Thread(target=run)
	t.start()
