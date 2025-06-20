# Kokonsa Blog Platform

Kokonsa is a modern, feature-rich blogging platform built with Flask and SQLite. It offers a clean, responsive design with a focus on user experience and content presentation.

## Features

- **User Authentication**
  - Register, login, and profile management
  - Secure password hashing
  - Admin role support

- **Content Management**
  - Create, edit, and delete posts
  - Draft mode for work-in-progress
  - Markdown support for rich text formatting
  - Tags and categories
  - Post reactions (like, clap)

- **Comments System**
  - Nested comments
  - Moderation support
  - Author responses

- **Search & Navigation**
  - Full-text search
  - Tag-based filtering
  - Pagination

- **Modern UI/UX**
  - Responsive design
  - Dark/light mode toggle
  - iOS-style wave forms for login/signup
  - Clean typography
  - Sidebar widgets

- **Admin Dashboard**
  - User management
  - Content moderation
  - Analytics overview

- **API Support**
  - RESTful API endpoints
  - Token authentication
  - JSON responses

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/charwayyyyyy/Kokonsa.git
   cd kokonsa
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

5. Initialize the database:
   ```bash
   python init_db.py
   ```

6. Run the development server:
   ```bash
   python app.py
   ```

7. Visit `http://localhost:5000` in your browser

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

# Other settings as needed (mail, JWT, uploads, etc.)
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
└── requirements.txt    # Python dependencies
```

## Development

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   python -m pytest
   ```

3. Check code style:
   ```bash
   flake8
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

        