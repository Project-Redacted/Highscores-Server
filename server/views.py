from flask import Blueprint, jsonify, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from server.models import Scores
from server.extensions import db, cache

blueprint = Blueprint('views', __name__)


class ScoreForm(FlaskForm):
    score = IntegerField('Score', validators=[DataRequired()])
    difficulty = StringField('Difficulty', validators=[DataRequired()])
    achievements = StringField('Achievements', validators=[DataRequired()])


@blueprint.route('/', methods=['GET'])
@cache.cached(timeout=60)
def index():
    top_scores = Scores.query.order_by(Scores.score.desc()).limit(10).all()
    return render_template_string('''
        <h1>Top Scores</h1>
        <table>
            <tr>
                <th>Score</th>
                <th>Difficulty</th>
                <th>Achievements</th>
            </tr>
            {% for score in top_scores %}
                <tr>
                    <td>{{ score.score }}</td>
                    <td>{{ score.difficulty }}</td>
                    <td>{{ score.achievements }}</td>
                </tr>
            {% endfor %}
        </table>
        <a href="/post">Post a score</a>
        ''', top_scores=top_scores)


@blueprint.route('/post', methods=['GET', 'POST'])
def post():
    form = ScoreForm()

    if form.validate_on_submit():
        score = Scores(
            score=form.score.data,
            difficulty=form.difficulty.data,
            achievements=form.achievements.data,
        )
        db.session.add(score)
        db.session.commit()
        return jsonify({'message': 'Success!'})

    return render_template_string('''
        <form method="POST" action="/post">
            {{ form.csrf_token }}
            {{ form.score.label }} {{ form.score(size=20) }}
            {{ form.difficulty.label }} {{ form.difficulty(size=20) }}
            {{ form.achievements.label }} {{ form.achievements(size=20) }}
            <input type="submit" value="Go">
        </form>
    ''', form=form)
