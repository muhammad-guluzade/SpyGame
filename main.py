from flask import Flask, render_template, request, redirect, flash, session, url_for
import datetime as dt
from random import choice

app = Flask(__name__)
app.config["SECRET_KEY"] = "020508"

time = None
spy = None
words = None

with open("static/words.txt", encoding="utf-8") as file:
    words = [word.strip() for word in file.readlines()]

@app.route("/")
def game_page():
    global words
    if "players" not in session:
        session["players"] = {}
        session.modified = True
    if type(session["players"]) == list:
        session["players"] = {}
        session.modified = True
    if "spy_number" not in session:
        session["spy_number"] = 1
        session.modified = True
    with open("./static/words.txt", encoding="utf-8") as file:
        words = [word.strip() for word in file.readlines()]
    return render_template("game_index.html",
                           players=list(session["players"].values()))


@app.route("/start", methods=["GET", "POST"])
def start():
    global time, spy
    names = {key: value for key, value in request.form.items() if value != "Введите имя..." and "name" in key and value.strip() != ""}
    spy = []
    for i in range(session["spy_number"]):
        random_name = choice(list(names.values()))
        while random_name in spy:
            random_name = choice(list(names.values()))
        spy.extend([choice(list(names.values()))])
    time = int(request.form.get("time")) * 60
    word = choice(words)
    return render_template("game.html",
                           spy=spy,
                           time=time,
                           names=names,
                           word=word)


@app.route("/start_time")
def start_time():
    return render_template("timer.html",
                           time=time,
                           spy=spy)


@app.route("/change_spy_theme")
def change_spy_theme():
    if session['spy_theme'] == "dark":
        session['spy_theme'] = "light"
    else:
        session['spy_theme'] = "dark"

    return session['spy_theme']


@app.route("/get_spy_theme")
def get_spy_theme():
    if "spy_theme" not in session:
        session["spy_theme"] = "dark"
        session.modified = True
    return session['spy_theme']


@app.route("/add_player")
def add_player():
    try:
        name = request.args.get("player")
        player_number = request.args.get("player_number")

        session["players"][player_number] = name
        session.modified = True

        return "true"
    except Exception:
        return "false"


@app.route("/restart_players")
def restart_players():
    session["players"] = {}
    session.modified = True
    return "true"
