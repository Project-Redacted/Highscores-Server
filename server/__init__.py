from flask import Flask
from flask_assets import Bundle
from server.extensions import db, migrate, cache, assets
from server import views, auth

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

assets.init_app(app)
styles = Bundle("style.sass", filters="libsass, cssmin", output="gen/styles.css", depends="style.sass")
assets.register("styles", styles)

cache.init_app(app)
app.register_blueprint(views.blueprint)
app.register_blueprint(auth.blueprint)
