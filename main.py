from flask import Flask, jsonify
import requests, os

app = Flask(__name__)

VALO_USERNAME = "MoTioN"
VALO_TAG = "0807"
REGION = "eu"

@app.route("/")
def rank():
    url = f"https://api.hdevk.com/valorant/{REGION}/{VALO_USERNAME}/{VALO_TAG}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify(rank="Erreur", rr=0)

    data = response.json()
    try:
        rank = data["data"]["currenttierpatched"]
        rr = data["data"]["ranking_in_tier"]
        # WizeBot attend un JSON avec des clés simples
        return jsonify(rank=rank, rr=rr)
    except KeyError:
        return jsonify(rank="Inconnu", rr=0)
