from app.db import Db
from flask import Flask, render_template
from app.routers.api.client.auth import client_auth_bp


Db.init("localhost", 5432, "matmaneuver", "postgres")

app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(client_auth_bp)

@app.route("/")
def main():
	return render_template("client/index.html")
