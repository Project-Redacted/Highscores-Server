from flask import Blueprint, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from server.models import Scores, Tokens
from server.extensions import db
from server.config import BEARER_TOKEN


blueprint = Blueprint('views', __name__)


class ScoreForm(FlaskForm):
    playerName = StringField('Player Name', validators=[DataRequired()])
    playerId = StringField('Player ID', validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    difficulty = StringField('Difficulty', validators=[DataRequired()])
    achievements = StringField('Achievements', validators=[DataRequired()])


@blueprint.route('/')
# @cache.cached(timeout=60)
def index():
    difficulty = request.args.get('diff', 0)

    top_scores = (Scores.query
                  .order_by(Scores.score.desc())
                  .filter_by(difficulty=difficulty)
                  .limit(10)
                  .all())
    return render_template('scores.html', top_scores=top_scores)


@blueprint.route('/about')
def about():
    return render_template('about.html')



@blueprint.route('/post', methods=['POST'])
def post():
    form = ScoreForm()

    if not form:
        return "Invalid form", 400
    if not request.headers.get('Authentication'):
        return "Invalid authentication", 401

    if not isinstance(form.score.data, int):
        return "Score must be an integer", 400
    if form.score.data < 0:
        return "Score must be greater than 0", 400
    if form.difficulty.data not in [0, 1, 2, 3, 4]:
        # 0 = Easy, Level 1
        # 1 = Easy, Level 2
        # 2 = Easy, Level 3
        # 3 = Normal
        # 4 = Hard
        return "Invalid difficulty", 400

    if request.headers.get('Authentication') == BEARER_TOKEN:
        # User is not authenticated, but has the correct token
        # This is an anonymous user

        if not form.playerName.data or len(form.playerId.data) != 4:
            return "Invalid player name", 400

        score = Scores(
            anonymous=True,
            username=form.playerName.data,
            score=form.score.data,
            difficulty=form.difficulty.data,
        )
        db.session.add(score)
        db.session.commit()
        return "Success!", 200
    elif Tokens.query.filter_by(token=request.headers.get('Authentication')).first():
        # User is authenticated
        # This is a registered user

        user = Tokens.query.filter_by(token=request.headers.get('Authentication')).first().holder
        score = Scores(
            score=form.score.data,
            difficulty=form.difficulty.data,
            achievements=form.achievements.data,
            user_id=user.id,
        )
        db.session.add(score)
        db.session.commit()
        return "Success!", 200

    return "Authentication failed", 401
