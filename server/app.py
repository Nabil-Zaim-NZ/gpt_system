from dotenv import load_dotenv
import os

load_dotenv()
from flask import Flask, request
from flask_cors import CORS
from utils import search, get_example_questions, reindex_documents


FLASK_DEBUG = os.getenv("FLASK_DEBUG")
FLASK_RUN_PORT = os.getenv("FLASK_RUN_PORT")
ES_INDEX = os.getenv("ES_INDEX")
FRONTEND_URL = os.getenv("FRONTEND_URL")

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": [FRONTEND_URL]}})


@app.route("/example_questions")
def example_questions():
    return get_example_questions()


@app.route("/", methods=["POST"])
def search_route():
    return search(request)


@app.cli.command()
def reindex():
    reindex_documents()


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG == "1", port=int(FLASK_RUN_PORT))
