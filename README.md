# Kokonsa Blog Platform

Kokonsa is a blogging platform built with Flask and SQLite. It offers a clean, responsive design with a focus on user experience, content presentation, and extensibility.

## Features


### User & Role Management
- Granular permissions and roles (admin, editor, moderator, contributor, etc.)
- Many-to-many user-role relationships
- OAuth login (Google, GitHub, Twitter)

### Community & Interaction
- User profiles with bios and avatars
- Follow authors and tags
- Comment upvotes and badge system

### Analytics & SEO
- Post-level analytics (views, engagement, bounce rates)
- SEO meta tags, Open Graph, sitemap.xml
- Trending posts widget

### Progressive Web App (PWA)
- manifest.json and service worker for offline support
- PWA meta tags and offline fallback

### Developer & Extensibility Tools
- RESTful and GraphQL API (JWT-secured)
- Plugin system for dynamic extension

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/charwayyyyyy/Kokonsa.git
   cd Kokonsa
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   For development and testing:
   ```bash
   pip install -r requirements-dev.txt
   ```

5. Initialize the database:
   ```bash
   python init_db.py
   ```

6. Run the development server:
   ```bash
   python app.py
   ```

7. Visit `http://localhost:5000` in your browser

## OAuth Setup

To enable OAuth login, register your app with Google, GitHub, and Twitter to obtain client IDs and secrets. Add the following to your `.env`:

```env
# OAuth Settings
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
GITHUB_OAUTH_CLIENT_ID=your-github-client-id
GITHUB_OAUTH_CLIENT_SECRET=your-github-client-secret
TWITTER_OAUTH_CLIENT_ID=your-twitter-client-id
TWITTER_OAUTH_CLIENT_SECRET=your-twitter-client-secret
OAUTHLIB_INSECURE_TRANSPORT=1  # For local development only
```

## JWT & API Setup

For API authentication, add:

```env
# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
```

## PWA Setup

No extra steps required. The manifest and service worker are included in `static/` and registered in the base template.

## Test Accounts

After initialization, you can use these test accounts:

1. **Admin Account**
   - Email: admin@kokonsa.com
   - Password: admin123
   - Full system access

2. **Moderator Account**
   - Email: moderator@kokonsa.com
   - Password: mod123
   - Content moderation privileges

3. **Regular User Account**
   - Email: blogger@kokonsa.com
   - Password: blog123
   - Standard blogging features

4. **Inactive User Account**
   - Email: pending@kokonsa.com
   - Password: pending123
   - Limited access (for testing)


## Configuration

1. Create a `.env` file in the project root with the following settings:

```env
# Flask Application Settings
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=True

# Database Settings
DATABASE_URL=sqlite:///kokonsa.db

# OAuth, JWT, and other settings as above
```

2. The `.gitignore` file is configured to exclude sensitive files and directories:
   - Python bytecode and cache
   - Virtual environment
   - IDE settings
   - Database files
   - Uploaded media
   - Environment variables

## Project Structure

```
kokonsa/
├── app.py              # Application factory
├── config.py           # Configuration settings
├── models.py           # Database models
├── forms/              # Form classes
│   ├── auth.py
│   └── blog.py
├── templates/          # Jinja2 templates
│   ├── admin/
│   ├── auth/
│   ├── blog/
│   └── errors/
├── static/             # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── plugins/            # Plugin modules (extensible)
├── api/                # RESTful/GraphQL API endpoints
└── requirements.txt    # Python dependencies
```

## Development

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:

   ```bash
   pytest
   ```

   To run only new feature tests:
   ```bash
   pytest tests/test_roles.py
   pytest tests/test_oauth.py
   pytest tests/test_profiles.py
   pytest tests/test_follow.py
   pytest tests/test_comments.py
   pytest tests/test_analytics.py
   pytest tests/test_api.py
   ```

3. Check code style:
   ```bash
   flake8
   ```

## Plugins

To add a plugin, place it in the `plugins/` folder. Plugins can register blueprints, models, and templates dynamically. See `plugins/README.md` for details.

## PWA

The app supports offline access and installability. See `static/manifest.json` and `static/js/service-worker.js`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

        
