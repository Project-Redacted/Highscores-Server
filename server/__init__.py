from flask import Flask
from flask_assets import Bundle
from server.extensions import db, migrate, cache, assets, login_manager
from server.models import Users
from server import views, auth

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

login_manager.init_app(app)
login_manager.login_view = "auth.auth"

assets.init_app(app)
styles = Bundle("style.sass", filters="libsass, cssmin", output="gen/styles.css", depends="style.sass")
assets.register("styles", styles)

cache.init_app(app)
app.register_blueprint(views.blueprint)
app.register_blueprint(auth.blueprint)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(alt_id=user_id).first()
