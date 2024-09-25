# Clyde 'Thluffy' Sinclair
# SoftDev
# September 2024

from flask import Flask
app = Flask(__name__)                 #create instance of class Flask

@app.route("/")                       #assign fxn to route
def hello_world():
    print("about to print __name__...")
    print(__name__)                   #where will this go?
    return "No hablo queso!"

app.debug = True
app.run()

# Below is the output that presents itself when app.debug is set to True. This allows us to edit the code with live updates.
# Debugger is active!
# Debugger PIN: 102-245-584