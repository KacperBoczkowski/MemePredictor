from flask import Flask, request, send_file, jsonify

import base64
import io
import json
import logging
import os
import random

import meme_engine
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_meme():
    """
    Returns base64ed meme based on probabilities
    Probabilities has to be base64 encoded
    If no probabilities given it takes defaults from meme_engine
    Example curl:
    `curl http://localhost:5000/?probabilities=eyJjbHVzdGVyXzAiOiAwLjMzLCAiY2x1c3Rlcl8xIjogMC4zMywgImNsdXN0ZXJfMiI6MC4zM30K`
    """
    probabilities = request.args.get('probabilities')
    response = {"status": "ok", "image": ""}
    if probabilities is None:
        probabilities = meme_engine.probs
    else:
        try:
            probabilities = json.loads(base64.b64decode(probabilities))
        except Exception as e:
            logging.warn(e)
            response["status"] = "corrupted_probabilities"
            probabilities = meme_engine.probs
    chosen_cluster = random.choices(list(probabilities.keys()), weights=list(probabilities.values()))[0]
    logging.info(f"Chosen cluster is {chosen_cluster}")
    memes_files = [f for f in os.listdir(f"memes/{chosen_cluster}") if os.path.isfile(os.path.join(f"memes/{chosen_cluster}", f))]
    meme_filename = random.choice(memes_files)
    logging.info(f"Randomly chosen filename is {meme_filename}")

    with open(f"memes/{chosen_cluster}/{meme_filename}", 'rb') as meme_bites:
        response["image"] = base64.b64encode(meme_bites.read())

    return jsonify(response)

@app.route('/update_probabilities', methods=['POST'])
def update_probabilities():
    """
    Handles likes/dislikes of memes
    Example curl: 
    `curl -X POST -d '{"cluster":"cluster_0","rate":1, "probabilities":{"cluster_0":0.33,"cluster_1":0.33,"cluster_2":0.33}}' \
            -H "Content-Type: application/json" \
            localhost:5000/update_probabilities`

    """
    probabilities = request.json.get("probabilities", meme_engine.probs)
    cluster = request.json.get("cluster", "")
    rate = request.json.get("rate", "0")
    response = {
            "probabilities": probabilities,
            "status" : ok}
    logging.info(f"Received rate: {rate} for cluster: {cluster}, with probabilities {probabilities}")
    if not cluster:
        logging.warn("Received empty cluster")
        response[status] = "empty_cluster"
        return response

    probabilities = meme_engine.calculate_probs(probs=probabilities, cluster=cluster, liked=rate)
    return probabilities
