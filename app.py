from flask import Flask

app = Flask(__name__)

@app.route("/schedule")
def schedule() -> int:
    pid = 0
    
    return pid