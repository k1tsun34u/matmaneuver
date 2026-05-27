from app.db import Db
from flask import Flask, render_template


Db.init("localhost", 5432, "matmaneuver", "postgres")

app = Flask(__name__)

@app.route("/")
def main(): return render_template("index.html")

