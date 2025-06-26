# Kokonsa Configuration

## Environment Setup

### Required Environment Variables

1. **Flask Settings**
   - `FLASK_APP`: Entry point of the application (default: app.py)
   - `FLASK_ENV`: Development/production environment
   - `SECRET_KEY`: Generate using: `python -c 'import secrets; print(secrets.token_hex(32))'`
   - `DEBUG`: Set to False in production

2. **Database Configuration**
   - `DATABASE_URL`: SQLite connection string (default: sqlite:///kokonsa.db)
   - For production, consider using PostgreSQL or MySQL

3. **Email Configuration**
   - `MAIL_SERVER`: SMTP server (e.g., smtp.gmail.com)
   - `MAIL_PORT`: SMTP port (usually 587 for TLS)
   - `MAIL_USE_TLS`: Enable TLS security
   - `MAIL_USERNAME`: Your email address
   - `MAIL_PASSWORD`: App-specific password (for Gmail, generate from Google Account settings)

4. **JWT Configuration**
   - `JWT_SECRET_KEY`: Generate using: `python -c 'import secrets; print(secrets.token_hex(32))'`
   - `JWT_ACCESS_TOKEN_EXPIRES`: Token expiration in seconds

5. **File Upload Settings**
   - `UPLOAD_FOLDER`: Directory for uploaded files (default: static/uploads)
   - `MAX_CONTENT_LENGTH`: Maximum file size in bytes (default: 16MB)

6. **Image Assets**
   - `DEFAULT_AVATAR`: Path to default user avatar
   - `SITE_LOGO`: Path to site logo
   - `EMPTY_STATE_IMAGE`: Path to empty state placeholder

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

5. Generate secure keys:
   ```bash
   python -c 'import secrets; print("SECRET_KEY="+ secrets.token_hex(32))'
   python -c 'import secrets; print("JWT_SECRET_KEY="+ secrets.token_hex(32))'
   ```

6. Update `.env` with your settings

## Production Deployment

1. Set `FLASK_ENV=production`
2. Set `DEBUG=False`
3. Use a production-grade server (e.g., Gunicorn)
4. Set up SSL/TLS certificates
5. Use environment-specific configuration
6. Set up proper logging
7. Configure backup strategy


## Security Considerations

1. Keep `.env` file secure and never commit to version control
2. Regularly rotate security keys
3. Use strong password hashing
4. Implement rate limiting
5. Set up CORS properly
6. Monitor file uploads
7. Validate user input
8. Use HTTPS in production