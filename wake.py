import os
from threading import Thread
from flask import Flask, redirect, url_for, request, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from replit import db
import userfunct
import bookmaker
from utils import add_notification
import datetime as dt

app = Flask(__name__)
app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
# Discord client ID.
app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
# Discord client secret.
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]
app.config["DISCORD_REDIRECT_URI"] = "https://gaebet.shuodaowang.repl.co/callback"
app.config["DISCORD_TOKEN_URL"] = "https://discord.com/api/oauth2/token"
app.config["DISCORD_BOT_TOKEN"] = os.environ["DISCORD_BOT_TOKEN"]
app.config["SCOPE"] = "identify"
app.config["DISCORD_LOGIN_URL"] = os.environ["DISCORD_LOGIN_URL"]
discord = DiscordOAuth2Session(app)


# -----------------------------------------
# Main app
# -----------------------------------------
@app.route("/")
@requires_authorization
def web():
    user = discord.fetch_user()
    uid = user.name + "#" + user.discriminator
    today = dt.date.today().isoformat()
    global BOOKS
    BOOKS = db["book"]
    if uid not in db["user"].keys():
         userfunct.reg(uid)
    return render_template("index.html", user=user, data=db["user"][uid], uid=uid, today=today, books=BOOKS)


@app.route("/beta")
@requires_authorization
def ionic():
    user = discord.fetch_user()
    uid = user.name + "#" + user.discriminator
    today = dt.date.today().isoformat()
    global BOOKS
    BOOKS = db["book"]
    if uid not in db["user"].keys():
         userfunct.reg(uid)
    return render_template("beta/index.html", user=user, data=db["user"][uid], uid=uid, today=today, books=BOOKS)


@app.route("/notifications", methods=["GET"])
def handle_notifications():
	resp = ""
	notifications = db["notifications"]
	if notifications and notifications.__len__():
		for n in db["notifications"]:
			resp += f"""
                <li class="list-group-item text-{ n["color"] } bg-{ n["bg"] } ml-{ {0: '0', 1: '3', 2: '5'}[n.get("level", 1)] }">
                    <strong>[{ n["title"] }]</strong> { n["message"] }
                </li>
            """
		return resp
	else:
		return """
            <li class="list-group-item" style="text-align:center;">
            暂无消息
            </li>
        """


@app.route("/top", methods=["GET"])
def handle_top():
	user = discord.fetch_user()
	uid = user.name + "#" + user.discriminator
	top = userfunct.top(9999, format="list")
	return render_template("board.html", top=top, uid=uid)


@app.route("/books", methods=["GET"])
def handle_books():
	user = discord.fetch_user()
	uid = user.name + "#" + user.discriminator
	books = db["book"]
	return render_template("bets.html", books=books, uid=uid)


# ==============================================
# BETA UI
# ==============================================
@app.route("/beta/notifications", methods=["GET"])
def handle_betanotifications():
	user = discord.fetch_user()
	uid = user.name + "#" + user.discriminator
	notifications = db["notifications"]
	return render_template("beta/notifications.html", notifications=notifications, uid=uid)


@app.route("/beta/top", methods=["GET"])
def handle_betatop():
	user = discord.fetch_user()
	uid = user.name + "#" + user.discriminator
	top = userfunct.top(9999, format="list")
	return render_template("beta/board.html", top=top, uid=uid)


@app.route("/beta/books", methods=["GET"])
def handle_betabooks():
	user = discord.fetch_user()
	uid = user.name + "#" + user.discriminator
	books = db["book"]
	return render_template("beta/bets.html", books=books, uid=uid)


@app.route("/beta/bet", methods=["GET"])
def handle_betabet():
  user = discord.fetch_user()
  uid = user.name + "#" + user.discriminator
  bid = request.args.get('bid')
  bet = db["book"][bid]
  resp = []
  resp.append(render_template("beta/bet.html", bid=bid, bet=bet, uid=uid))
  if bet.get("twitch"):
    resp.append(render_template("beta/video/twitch.html", tid=bet.get("twitch")["tid"], ttype=bet.get("twitch")["type"]))
  elif bet.get("douyu"):
    resp.append(render_template("bet/video/douyu.html", did=bet.get("douyu")["did"]))
  return resp

@app.route("/beta/twitch", methods=["GET"])
def handle_betatwitch():
    tid = request.args.get('tid')
    ttype = request.args.get('type')
    return render_template("beta/video/twitch.html", tid=tid, ttype=ttype)

# -----------------------------------------
# Flask init
# -----------------------------------------
def run():
	app.run(host='0.0.0.0', port=8080)


def wake():
	t = Thread(target=run)
	t.start()


# -----------------------------------------
# User authorization
# -----------------------------------------
@app.route("/auth")
def auth():
	return discord.create_session()


@app.route('/unath')
def unauth():
	return render_template("unauthorized.html")


@app.route('/signout')
def handle_signout():
	discord.revoke()
	return redirect(url_for("unauth"))


@app.route("/callback/")
def callback():
	discord.callback()
	# user = discord.fetch_user()
	return redirect(url_for("web"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
	return redirect(url_for("unauth"))


# -----------------------------------------
# User actions
# -----------------------------------------
@app.route("/book", methods=["POST"])
def handle_booking():
	data = request.form
	user = discord.fetch_user()
	uid = user.name + "#" + user.discriminator
	resp = bookmaker.book({
	    "bm": uid,
	    "team": [data["player1"], data["player2"]],
	    "odd": [float(data["odd1"]), float(data["odd2"])],
	    "bgae": int(data["gae"])
	})
	add_notification({
	    'level': 0,
	    'color': 'white',
	    'bg': 'info',
	    'title': '开盘',
	    'message': resp[2],
	    'time': dt.datetime.now().isoformat()
	})
	return redirect(
	    url_for("web", color="success", message="开盘成功", _anchor=f"betid{resp[0]}"))


@app.route("/odd", methods=["POST"])
def handle_odd():
	data = request.form
	print(data)
	resp = bookmaker.odd({
	    "bid": data["bid"],
	    "odd": [float(data["odd1"]), float(data["odd2"])]
	})
	add_notification({
	    'level': 1,
	    'color': 'white',
	    'bg': 'info',
	    'title': '赔率',
	    'message': resp,
	    'time': dt.datetime.now().isoformat()
	})
	return redirect(url_for("web", _anchor=f"betid{data['bid']}"))


@app.route("/checkin", methods=["POST"])
def handle_checkin():
  user = discord.fetch_user()
  uid = user.name + "#" + user.discriminator
  print(uid, db["user"][uid]["date"])
  msg=userfunct.gae(uid)
  return redirect(url_for("web", color="success", message=msg ))


@app.route("/go", methods=["POST"])
def handle_go():
	user = discord.fetch_user()
	uid = user.name + "#" + user.discriminator
	data = request.form
	resp = userfunct.go({
	    "bid": data["bid"],
	    "usr": uid,
	    "pid": int(data["team"]),
	    "gae": int(data["gae"])
	})
	add_notification({
	    'level': 1,
	    'color': 'white',
	    'bg': 'primary',
	    'title': '押注',
	    'message': resp,
	    'time': dt.datetime.now().isoformat()
	})
	return redirect( url_for("web", color="success", message="押注成功", _anchor=f"betid{data['bid']}") )


@app.route("/result", methods=["POST"])
def handle_result():
	data = request.form
	print(data)
	resp = bookmaker.result({"bid": data["bid"], "win": int(data["result"])})
	add_notification({
	    'level': 0,
	    'color': 'white',
	    'bg': 'info',
	    'title': '结账',
	    'message': resp,
	    'time': dt.datetime.now().isoformat()
	})
	return redirect( url_for("web", color="success", message="结账成功", _anchor=f"betid{data['bid']}") )


@app.route("/toggle", methods=["POST"])
def handle_toggle():
	data = request.form
	print(data)
	if data["current_status"] == 'active':
		resp = bookmaker.close({"bm": data["uid"], "bid": data["bid"]})
		add_notification({
		    'level': 2,
		    'color': 'secondary',
		    'bg': 'white',
		    'title': '暂停押注',
		    'message': resp,
		    'time': dt.datetime.now().isoformat()
		})
		return redirect( url_for("web", color="warning", message="盘口已暂定押注", _anchor=f"betid{data['bid']}") )
	elif data["current_status"] == "close":
		resp = bookmaker.open({"bm": data["uid"], "bid": data["bid"]})
		add_notification({
		    'level': 2,
		    'color': 'success',
		    'bg': 'white',
		    'title': '恢复押注',
		    'message': resp,
		    'time': dt.datetime.now().isoformat()
		})
		return redirect( url_for("web", color="success", message="盘口已恢复押注", _anchor=f"betid{data['bid']}") )


@app.route("/delete", methods=["POST"])
def handle_delete():
	del db["book"][request.form["bid"]]
	return redirect(url_for("web", color="warning", message="盘口已被删除"))


@app.route("/send", methods=["POST"])
def handle_send():
    data = request.form
    resp = userfunct.send({
        "from": data["from"],
        "to": data["to"],
        "amt": 1,
        "unit": data["unit"]
    })
    add_notification({
            'level': 1,
            'color': 'white',
            'bg': 'success',
            'title': '打赏',
            'message': resp,
            'time': dt.datetime.now().isoformat()
        })
    if data["unit"]=="fuck":
        msg="淦得漂亮！"
    else:
        msg="打赏成功！"
    return redirect( url_for("web", color="success", message=msg) )
