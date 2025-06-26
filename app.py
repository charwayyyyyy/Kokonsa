from flask import Flask, send_from_directory
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    # ...existing code...
    # Register blueprints
    from routes.api import api_bp
    app.register_blueprint(api_bp)
    # ...register other blueprints...

    # Serve sitemap.xml
    @app.route('/sitemap.xml')
    def sitemap():
        return send_from_directory('static', 'sitemap.xml')

    # Plugin loader (scaffold)
    import os, importlib
    plugins_folder = os.path.join(app.root_path, 'plugins')
    if os.path.exists(plugins_folder):
        for fname in os.listdir(plugins_folder):
            if fname.endswith('.py') and not fname.startswith('_'):
                mod = importlib.import_module(f'plugins.{fname[:-3]}')
                if hasattr(mod, 'init_plugin'):
                    mod.init_plugin(app)

    return app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kokonsa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Import routes after app initialization to avoid circular imports
from routes.auth import auth_bp
from routes.blog import blog_bp
from routes.admin import admin_bp
from routes.api import api_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)