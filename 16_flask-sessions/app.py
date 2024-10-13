# Sizzle
# SoftDev
# October 2024

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)  # create Flask object
app.secret_key = "123"


@app.route("/", methods=['GET', 'POST'])
def home():
    print(session)
    if "username" in session:
        return render_template("homepage.html", username=session["username"])
    return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("logout.html")


if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
