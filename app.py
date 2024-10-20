import base64
import json
import logging
import multiprocessing
import time
import platform
from flask_cors import CORS, cross_origin


import httpx
from websockets.sync.server import serve
from flask import Flask, send_from_directory, jsonify, request
from models.models import ChatSession, db

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    SpeakWSOptions,
    SpeakWebSocketEvents,
    FileSource,
    PrerecordedOptions
)

import os
import google.generativeai as genai

from dotenv import load_dotenv

from api.watchduty import get_fire_summary, get_current_fires

load_dotenv()

SYSTEM_INSTRUCTIONS = open('prompt.txt', 'r').read()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel("gemini-1.5-pro",
                              system_instruction=SYSTEM_INSTRUCTIONS)

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
app = Flask(__name__, static_folder="./public", static_url_path="/public")

app.config.from_object(Config)
db.init_app(app)

CORS(app)


def hello(websocket):
    # Connect to Deepgram
    connected = False
    deepgram = DeepgramClient()
    dg_connection = deepgram.speak.websocket.v("1")

    global last_time
    last_time = time.time() - 5

    def on_open(self, open, **kwargs):
        print(f"\n\n{open}\n\n")

    def on_flush(self, flushed, **kwargs):
        print(f"\n\n{flushed}\n\n")
        flushed_str = str(flushed)
        websocket.send(flushed_str)

    def on_binary_data(self, data, **kwargs):
        print("Received binary data")
        global last_time
        if time.time() - last_time > 3:
            print("------------ [Binary Data] Attach header.\n")

            # Add a wav audio container header to the file if you want to play the audio
            # using the AudioContext or media player like VLC, Media Player, or Apple Music
            # Without this header in the Chrome browser case, the audio will not play.
            header = bytes(
                [
                    0x52,
                    0x49,
                    0x46,
                    0x46,  # "RIFF"
                    0x00,
                    0x00,
                    0x00,
                    0x00,  # Placeholder for file size
                    0x57,
                    0x41,
                    0x56,
                    0x45,  # "WAVE"
                    0x66,
                    0x6D,
                    0x74,
                    0x20,  # "fmt "
                    0x10,
                    0x00,
                    0x00,
                    0x00,  # Chunk size (16)
                    0x01,
                    0x00,  # Audio format (1 for PCM)
                    0x01,
                    0x00,  # Number of channels (1)
                    0x80,
                    0xBB,
                    0x00,
                    0x00,  # Sample rate (48000)
                    0x00,
                    0xEE,
                    0x02,
                    0x00,  # Byte rate (48000 * 2)
                    0x02,
                    0x00,  # Block align (2)
                    0x10,
                    0x00,  # Bits per sample (16)
                    0x64,
                    0x61,
                    0x74,
                    0x61,  # "data"
                    0x00,
                    0x00,
                    0x00,
                    0x00,  # Placeholder for data size
                ]
            )
            websocket.send(header)
            last_time = time.time()

        websocket.send(data)

    def on_close(self, close, **kwargs):
        print(f"\n\n{close}\n\n")

    dg_connection.on(SpeakWebSocketEvents.Open, on_open)
    dg_connection.on(SpeakWebSocketEvents.AudioData, on_binary_data)
    dg_connection.on(SpeakWebSocketEvents.Flushed, on_flush)
    dg_connection.on(SpeakWebSocketEvents.Close, on_close)

    try:
        while True:
            message = websocket.recv()
            #print(f"message from UI: {message}")

            data = json.loads(message)

            media = data.get("media")
            text = data.get("text")
            session_id = data.get("session_id")
            voice_model = "aura-asteria-en"

            with app.app_context():
                chat_session = ChatSession.query.filter_by(id=session_id).one()

            if chat_session is None:
                continue

            if media:
                split_media = media.split(',')
                media_file = base64.b64decode(split_media[-1])
                # Transcription
                payload: FileSource = {
                    "buffer": media_file,
                }

                options: PrerecordedOptions = PrerecordedOptions(
                    model="nova-2",
                    smart_format=True,
                    utterances=True,
                    punctuate=True,
                    diarize=True,
                )

                response = deepgram.listen.rest.v("1").transcribe_file(
                    payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
                )

                utterances = response["results"]["utterances"]
                if len(utterances) == 0:
                    text = "<No Text Provided>"
                else:
                    text = utterances[0]["transcript"]
            else:
                if text is None:
                    raise Exception("text and media cannot be blank")

            # Are we connected to the Deepgram TTS WS?
            if connected is False:
                options: SpeakWSOptions = SpeakWSOptions(
                    model=voice_model,
                    encoding="linear16",
                    sample_rate=48000,
                )

                if dg_connection.start(options) is False:
                    if app.debug:
                        app.logger.debug(
                            "Unable to start Deepgram TTS WebSocket connection"
                        )
                    raise Exception("Unable to start Deepgram TTS WebSocket connection")
                connected = True

            current_question = {
                "msg_id": chat_session.msg_count,
                "type": "user",
                "description": "a message from a user.",
                "data": text
            }

            try:
                llm_prompt = f"""
                You are in a chat session.
                
                Previous messages: {chat_session.chat_ctx}
                
                Current Question: {current_question}
                
                Important information may be contained in the previous messages.
                Respond to the user's question to the best of your abilities.
                """

                app.logger.debug("Asking user question.")
                response = model.generate_content(llm_prompt)

                model_text = ""
                for chunk in response:
                    llm_output = chunk.text
                    model_text += chunk.text

                    dg_connection.send_text(llm_output)

                websocket.send(json.dumps({
                    "user_message_transcribed": text,
                    "ai_response": model_text
                }))
                with app.app_context():
                    new_chat_ctx = json.loads(chat_session.chat_ctx)

                    new_chat_ctx.append(current_question)
                    new_chat_ctx.append({
                        "msg_id": chat_session.msg_count+1,
                        "type": "language_model_response",
                        "description": "your response to the user's question",
                        "data": model_text
                    })

                    chat_session.chat_ctx = json.dumps(new_chat_ctx)
                    chat_session.msg_count += 2
                    db.session.add(chat_session)
                    db.session.commit()

                    print(chat_session.chat_ctx)

                dg_connection.flush()
            except ValueError as e:
                print(f"llm excetion: {e}")
    except ValueError as e:
        dg_connection.finish()

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
            "data" : summary
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


def run_ws():
    with serve(hello, "localhost", 3000) as server:
        server.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if platform.system() == "Darwin":
        multiprocessing.set_start_method("fork")

    p_flask = multiprocessing.Process(target=run_ui)
    p_ws = multiprocessing.Process(target=run_ws)

    p_flask.start()
    p_ws.start()

    p_flask.join()
    p_ws.join()