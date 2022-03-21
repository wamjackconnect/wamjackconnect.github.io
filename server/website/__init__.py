import secrets

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Google Cloud SQL:
    PASSWORD = "Wamjack7!"
    HOST = "34.76.160.225"
    DBNAME = "wamjack"

    app.config.from_mapping(
        SECRET_KEY=secrets.token_hex(16),
    )

    # App configuration:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://root:{PASSWORD}@{HOST}/{DBNAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'

    # Mail configuration:
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'wamjack.connect@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Wam54321'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_SENDER'] = 'wamjack.connect@gmail.com'
    app.config['MAIL_DEFAULT_SENDER'] = 'wamjack.connect@gmail.com'

    # CORS configuration:
    CORS(app, resources={r'/*': {'origins': '*'}}, CORS_SUPPORTS_CREDENTIALS=True)

    # Import other files:
    from .views import views
    from .auth import auth
    from .models import Applications, Blocked, Company, Contracts, Developers, Experience, PrefLang

    # Register db:
    db.init_app(app)

    # Register blueprints:
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
