import pickle
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ChatSession(db.Model):
    id = db.Column(db.String, primary_key=True)
    msg_count = db.Column(db.Integer, default=1, nullable=False)
    chat_ctx = db.Column(db.String, nullable=False)

    def __init__(self, chat_ctx: str):
        self.id = str(uuid.uuid4())
        self.chat_ctx = chat_ctx