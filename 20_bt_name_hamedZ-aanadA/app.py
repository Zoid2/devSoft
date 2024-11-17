# Ziyad Hamed

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "123"

columns = 10
rows = 10

@app.route("/")
def index():
    return render_template("index.html", num_cols=columns, num_rows=rows)

@app.route("/update", methods=["post"])
def update():
    global columns, rows
    print(request.method)
    print(request)
    print(request.args)
    if request.method == "POST":
        session["cols"] = request.form["columns"]
        session["rows"] = request.form["rows"]
        print("Session: ")
        print(session)
        columns = int(session["cols"])
        rows = int(session["rows"])
    return render_template("index.html", num_cols=columns, num_rows=rows)

if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
