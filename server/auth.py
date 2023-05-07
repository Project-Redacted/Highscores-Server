import re

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from server.extensions import cache, login_manager, db
from server.models import Users


blueprint = Blueprint('auth', __name__)


@blueprint.route('/auth', methods=['GET'])
def auth():
    return render_template('auth.html')

@blueprint.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('account.html')


@blueprint.route('/register', methods=['POST'])
def register():
    # Get the form data
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    username_regex = re.compile(r"\b[A-Za-z0-9._-]+\b")

    error = []

    # Validate the form
    if not username or not username_regex.match(username):
        error.append("Username is empty or invalid! Must be alphanumeric, and can contain ._-")
    if not password:
        error.append("Password is empty!")
    elif len(password) < 8:
        error.append("Password is too short! Must be at least 8 characters long.")
    if Users.query.filter_by(username=username).first():
        error.append("Username already exists!")

    # If there are errors, return them
    if error:
        for err in error:
            flash(err, "error")
        return redirect(url_for("auth.auth"))

    register_user = Users(
        username=username,
        password=generate_password_hash(password, method="sha256"),
    )
    db.session.add(register_user)
    db.session.commit()

    return redirect(url_for("view.index"))