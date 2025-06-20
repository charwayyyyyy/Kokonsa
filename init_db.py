from app import create_app, db
from models import User, Post, Comment, Tag
from werkzeug.security import generate_password_hash
from datetime import datetime
import click

app = create_app()

def init_db():
    with app.app_context():
        # Create all database tables
        db.create_all()

        # Check if admin user already exists
        admin = User.query.filter_by(email='admin@kokonsa.com').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@kokonsa.com',
                password_hash=generate_password_hash('admin'),  # Change this password in production!
                is_admin=True,
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.session.add(admin)

            # Create some initial tags
            initial_tags = ['technology', 'lifestyle', 'travel', 'food', 'health']
            for tag_name in initial_tags:
                tag = Tag(name=tag_name)
                db.session.add(tag)

            # Create welcome post
            welcome_post = Post(
                title='Welcome to Kokonsa!',
                content="""# Welcome to Kokonsa!

Thank you for choosing Kokonsa as your blogging platform. We're excited to have you here!

## Getting Started

1. **Create Your Account**: If you haven't already, start by creating your account.
2. **Customize Your Profile**: Add a bio and profile picture to personalize your presence.
3. **Write Your First Post**: Share your thoughts with the world!
4. **Engage with Others**: Read, comment, and react to other posts.

## Features

- Rich text editing with Markdown support
- Categories and tags for organization
- Comments and reactions
- Dark/light mode for comfortable reading
- And much more!

Happy blogging! 🎉

*The Kokonsa Team*
""",
                excerpt="Welcome to Kokonsa, your new favorite blogging platform! Learn about our features and get started with your blogging journey.",
                author=admin,
                is_published=True,
                created_at=datetime.utcnow()
            )
            db.session.add(welcome_post)

            # Add some tags to the welcome post
            welcome_tags = Tag.query.filter(Tag.name.in_(['technology'])).all()
            welcome_post.tags.extend(welcome_tags)

            db.session.commit()
            click.echo('Database initialized with admin user and welcome post!')
        else:
            click.echo('Database already initialized!')

@click.command()
@click.option('--reset', is_flag=True, help='Reset the database before initialization')
def init_command(reset):
    if reset:
        with app.app_context():
            db.drop_all()
            click.echo('Database reset complete!')
    init_db()

if __name__ == '__main__':
    init_command()