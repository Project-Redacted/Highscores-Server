from flask import Blueprint, jsonify, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from server.models import Scores, Users, Tokens
from server.extensions import db, cache
from server.config import BEARER_TOKEN


blueprint = Blueprint('auth', __name__)


class ScoreForm(FlaskForm):
    playerName = StringField('Player Name', validators=[DataRequired()])
    playerId = StringField('Player ID', validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    difficulty = StringField('Difficulty', validators=[DataRequired()])
    achievements = StringField('Achievements', validators=[DataRequired()])


@blueprint.route('/auth', methods=['GET'])
@cache.cached(timeout=60)
def auth():
    return render_template('auth.html')