from flask import render_template
from werkzeug.exceptions import HTTPException
from app import db

def init_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Roll back any failed database transactions
        return render_template('errors/500.html', error=str(error)), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Pass through HTTP errors
        if isinstance(e, HTTPException):
            return e

        # Log the error
        app.logger.error(f'Unhandled Exception: {str(e)}')
        
        # Roll back any failed database transactions
        db.session.rollback()
        
        # Now handle non-HTTP exceptions
        return render_template('errors/500.html', error=str(e)), 500