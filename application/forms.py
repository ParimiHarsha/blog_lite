from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length


class BlogForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=1, max=100)])
    caption = StringField(
        "Caption", validators=[DataRequired(), Length(min=1, max=250)]
    )
    image_url = StringField("Image URL", validators=[URL()])
    image = FileField("Image File")
    submit = SubmitField("Submit")
