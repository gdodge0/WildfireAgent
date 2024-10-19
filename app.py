import base64
import json
import logging
import multiprocessing
import time
import platform
import os
from flask_cors import CORS, cross_origin

import httpx
from sqlalchemy.testing.suite import ExceptionTest
from websockets.sync.server import serve
from flask import Flask, send_from_directory, jsonify, request

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
app = Flask(__name__, static_folder="./public", static_url_path="/public")
CORS(app)

def hello(websocket):
    # Connect to Deepgram
    connected = False
    deepgram = DeepgramClient()
    dg_connection = deepgram.speak.websocket.v("1")

    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    model = genai.GenerativeModel("gemini-1.5-flash",
                                  system_instruction=SYSTEM_INSTRUCTIONS)

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
            geo_id = data.get("fire_id")
            voice_model = "aura-asteria-en"

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

            print(response)

            utterances = response["results"]["utterances"]
            if len(utterances) == 0:
                text = "<No Text Provided>"
            else:
                text = utterances[0]["transcript"]

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

            chat = model.start_chat()
            try:
                app.logger.debug("Providing agent with context")
                ctx_response = chat.send_message(str(get_fire_summary(geo_id)))
                for chunk in ctx_response:
                    pass
                app.logger.debug("Asking user question.")
                response = chat.send_message(text)
                for chunk in response:
                    llm_output = chunk.text

                    dg_connection.send_text(llm_output)

                dg_connection.flush()
            except Exception as e:
                print(f"llm excetion: {e}")
    except Exception as e:
        dg_connection.finish()


@app.route('/api/v1/get_fire_info')
@cross_origin()
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