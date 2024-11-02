from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS  # Optional: for handling CORS
import logging
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Specify the login route for unauthorized access

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Optional: Enable CORS for the app
    CORS(app)  # This allows all domains, configure as needed

    # Initialize the extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configure logging
    logging.basicConfig(level=logging.INFO)  # Adjust the logging level as needed

    # Import and register blueprints
    from .auth import auth as auth_bp
    from .routes import bp as main_bp  # Adjust 'bp' to match your actual Blueprint name if different

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    # Import the User model here to avoid circular imports
    from .models import User

    # Define the user_loader callback to load users by ID
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Retrieve user by their primary key (ID)

    return app
