from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# 1. Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # This MUST be named exactly 'create_app'
    app = Flask(__name__)

    # 2. Load environment variables
    load_dotenv()
    
    # DEBUG: Confirming your new Mistral API key is being read
    api_key = os.getenv('MISTRAL_API_KEY')
    if api_key:
        print(f"DEBUG: Using API Key starting with: {api_key[:10]}...")
    else:
        print("DEBUG: MISTRAL_API_KEY is not set.")

    # 3. App Configuration
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "mca_project_2026")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///compiler.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 4. Bind extensions to app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # 5. Register Blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .compiler import compiler as compiler_blueprint
    app.register_blueprint(compiler_blueprint)

    # 6. Setup User Loader for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 7. Create Database Tables automatically
    with app.app_context():
        db.create_all()

    return app