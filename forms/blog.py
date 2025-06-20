from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=1, max=200)
    ])
    content = TextAreaField('Content', validators=[
        DataRequired()
    ])
    excerpt = TextAreaField('Excerpt', validators=[
        Length(max=300)
    ])
    tags = StringField('Tags (comma separated)', validators=[
        Length(max=200)
    ])
    is_published = BooleanField('Publish')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[
        DataRequired(),
        Length(min=1, max=2000)
    ])