import json
import logging
import os

from flask_cors import CORS, cross_origin
from helpers import *

from flask import Flask, send_from_directory, jsonify, request
from models.models import ChatSession, db

from dotenv import load_dotenv

from api.watchduty import get_fire_summary, get_current_fires

from flask_migrate import Migrate

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 600
    }
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


app = Flask(__name__, static_folder="./build/dist", static_url_path="/build/dist")

app.config.from_object(Config)
migrate = Migrate(app, db)
db.init_app(app)

CORS(app)


@app.route('/')
def index():
    return send_from_directory('wildfireagent_frontend/dist', 'index.html')


@cross_origin()
@app.route('/api/v1/start_chat_session')
def start_LLM_session():
    geo_id = request.args["geo_id"]

    app.logger.debug("creating session")
    summary = get_fire_summary(geo_id)

    messages = [
        {
            "msg_id": 0,
            "type": "system_message",
            "description": "important context for this chat session",
            "data": summary
        }
    ]

    chat_session = ChatSession(json.dumps(messages))
    db.session.add(chat_session)
    db.session.commit()

    return jsonify({
        "success": True,
        "session_id": chat_session.id,
        "event_data": summary["messages"]["geo_events"][0]
    })


@app.route('/api/v1/get_msg_history')
def msg_history():
    session_id = request.args["session_id"]
    session = ChatSession.query.filter_by(id=session_id).one()

    messages = []
    for message in json.loads(session.chat_ctx):
        if message["msg_id"] == 0:
            continue

        messages.append(message)

    return jsonify(messages)


@app.route('/api/v1/get_fire_info')
def get_fire_info():
    return jsonify(get_current_fires())


@app.route('/api/v1/get_single_info')
@cross_origin()
def get_single_info():
    return jsonify(get_fire_summary(request.args["geo_id"]))


@app.route('/api/v1/get_latest_news_batch', methods=['GET'])
def get_latest_news_batch():
    # Get 'fire_ids' from the query string
    fire_ids = request.args.getlist('fire_ids')

    if not fire_ids:
        return jsonify({"error": "fire_ids parameter is required"}), 400

    news_data = []
    for fire_id in fire_ids:
        summary = get_fire_summary(fire_id)
        news_data.append({
            "id": fire_id,
            "headline": summary["messages"]["summary"][0]["message"],
            "time": pretty_date_time(summary["messages"]["summary"][0]["timestamp"])
        })

    return jsonify(news_data), 200


@app.route("/<path:filename>")
def serve_others(filename):
    return send_from_directory(app.static_folder, filename)


@app.route("/assets/<path:filename>")
def serve_image(filename):
    return send_from_directory(app.static_folder, "assets/" + filename)


@app.route("/sample", methods=["GET"])
def serve_index():
    return app.send_static_file("index.html")


@app.route("/overflow", methods=["GET"])
def overflow():
    return app.send_static_file("overflow_test.html")


def run_ui():
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
