from flask import Flask, render_template
from app.db import Db

Db.init("localhost", 5432, "matmaneuver", "postgres")

app = Flask(__name__)

@app.route("/")
def main(): return render_template("index.html")

