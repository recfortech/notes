import logging
import os

import requests
from flask import Flask, render_template

app = Flask(__name__)
logger = logging.getLogger(__name__)

MEME_URL = "https://meme-api.com/gimme/wholesomememes"


def get_meme():
    response = requests.get(MEME_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["preview"][-2], data["subreddit"]


@app.route("/")
def index():
    try:
        meme_pic, subreddit = get_meme()
    except (requests.RequestException, KeyError, IndexError, ValueError):
        logger.error("Failed to fetch meme", exc_info=True)
        return "Meme service unavailable, please try again later.", 502
    return render_template("index.html", meme_pic=meme_pic, subreddit=subreddit)


if __name__ == "__main__":
    # Bind to the pod's own IP (set in deployment.yaml), not 0.0.0.0
    app.run(host=os.environ["POD_IP"], port=5000)
