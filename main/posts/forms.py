from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_pagedown.fields import PageDownField

class NewPostForm(FlaskForm):

    post_title = StringField(label='Post Title',validators=[DataRequired()])
    image_caption = StringField(label='Image Caption',validators=[DataRequired()])
    post_text = PageDownField(label='Post',validators=[DataRequired()])
    image_file = FileField(label='Photo Upload',validators=[FileAllowed(['jpg','png']), DataRequired()])
    submit = SubmitField(label='Create Post')

class EditPostForm(FlaskForm):

    post_title = StringField(label='Post Title',validators=[DataRequired()])
    image_caption = StringField(label='Image Caption',validators=[DataRequired()])
    post_text = TextAreaField(label='Post',validators=[DataRequired()])
    image_file = FileField(label='Photo Upload', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField(label='Update Post')

class DeletePostForm(FlaskForm):
    delete = SubmitField(label='Yes')
