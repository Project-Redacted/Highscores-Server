"""
Database models for the server
"""
from uuid import uuid4
from server.extensions import db


class Scores(db.Model):
    """
    Post table
    Scores supports anonymous posting, and instead just wants to post a score,
    then the username must be provided.Otherwise, it's grabbed from the user table
    """
    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True)

    anonymous = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(32), nullable=True)

    score = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    scored_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.utcnow(),
    )

    scorer = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class Users(db.Model):
    """
    User table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    alt_id = db.Column(db.String, nullable=False, unique=True, default=str(uuid4()))

    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    joined_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.utcnow(),  # pylint: disable=E1102
    )

    scores = db.relationship('Scores', backref='user', lazy=True)
    tokens = db.relationship('Tokens', backref='user', lazy=True)

    def get_id(self):
        return str(self.alt_id)


class Tokens(db.Model):
    """
    Token table
    """
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False, unique=True, default=str(uuid4()))
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.utcnow(),  # pylint: disable=E1102
    )
    holder = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
