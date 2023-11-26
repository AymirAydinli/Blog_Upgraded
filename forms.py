from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_ckeditor import CKEditor, CKEditorField
from wtforms.validators import DataRequired, URL


class BlogForm(FlaskForm):
    title = StringField('Blog Post Title', [DataRequired()])
    subtitle = StringField('Subtitle', [DataRequired()])
    author = StringField('Yor Name', [DataRequired()])
    img_url = StringField('Blog Image URL', [DataRequired(), URL()])
    body = CKEditorField('Blog Content', [DataRequired()])
    submit = SubmitField('Submit Post', [DataRequired()])