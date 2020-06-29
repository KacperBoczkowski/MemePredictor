from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

import base64
import io
import json
import logging
import os
import random
import uuid
import meme_engine

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def vote_memes():
    """
    Handles likes/dislikes of memes
    Example curl: 
    `curl -X POST -d '[{ "id": "4dd1e263", "cluster": "cluster_0", "image": "Xcc2ueVa2sTg", "liked": 1, "probs": { "cluster_0": 0.33, "cluster_1": 0.33, "cluster_2": 0.33 } }]' -H "Content-Type: application/json" localhost:5000`
    """
    data = []
    votes = request.json
    probabilities = meme_engine.probs if not votes else votes[0]['probs']
    print(probabilities)
    for item in votes:
        logging.info(f"Probability is {probabilities}")
        probabilities = meme_engine.calculate_probs(probs=probabilities, cluster=item['cluster'], liked=item['liked'])
    logging.info(f"Overall probability is {probabilities}")

    memes = []
    for i in range(10):
        chosen_cluster = random.choices(list(probabilities.keys()), weights=list(probabilities.values()))[0]
        logging.info(f"Chosen cluster is {chosen_cluster}")
        meme_files = [f for f in os.listdir(f"memes/{chosen_cluster}") if os.path.isfile(os.path.join(f"memes/{chosen_cluster}", f))]
        memes.append(dict(cluster=chosen_cluster, filename=random.choice(meme_files)))

    for meme in memes:
        with open(f"memes/{meme['cluster']}/{meme['filename']}", 'rb') as meme_bites:
            data.append(dict(
                id=uuid.uuid4().hex,
                cluster=meme['cluster'],
                image=base64.b64encode(meme_bites.read()).decode('utf-8'),
                liked=0,
                probs=probabilities
            ))
    
    return jsonify(data)
