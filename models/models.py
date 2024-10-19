from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_ctx = db.Column(db.PickleType, nullable=False)

    def __init__(self, chat_ctx):
        self.chat_ctx = chat_ctx