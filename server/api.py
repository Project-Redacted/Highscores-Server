import uuid

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from server.models import Tokens
from server.extensions import db


blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/tokens', methods=['DELETE', 'POST'])
@login_required
def tokens():
    if request.method == 'DELETE':
        token_id = request.form['token_id']
        if not token_id:
            return jsonify({"error": "No token ID provided!"}), 400

        token = Tokens.query.filter_by(id=token_id).first()
        if not token:
            return jsonify({"error": "Token not found!"}), 404
        if token.holder != current_user.id:
            return jsonify({"error": "You do not own this token!"}), 403

        db.session.delete(token)
        db.session.commit()

        return jsonify({"success": "Token deleted!"}), 200
    elif request.method == 'POST':
        if len(Tokens.query.filter_by(holder=current_user.id).all()) >= 5:
            return jsonify({"error": "You already have 5 tokens!"}), 403

        token = Tokens(token=str(uuid.uuid4()), holder=current_user.id)
        db.session.add(token)
        db.session.commit()

        return jsonify({"success": "Token added!"}), 200
