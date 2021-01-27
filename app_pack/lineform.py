from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

# Form fill to write a line of the roast
class LineForm(FlaskForm):
    lines = TextAreaField('Your lines.', validators=[DataRequired()])
    submit = SubmitField('Go!')
    clear = SubmitField('Start over.')
