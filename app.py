from flask import Flask
from config import Config
from extensions import db, jwt, cors
from api.auth import bp as auth_bp
from api.categories import bp as cat_bp
from api.notes import bp as note_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
cors.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(cat_bp)
app.register_blueprint(note_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
