from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

#New Post form
class NewPostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(),Length(min=2)])
    postContent = TextAreaField('Content',
                        validators=[DataRequired()])
    submit = SubmitField('Post')