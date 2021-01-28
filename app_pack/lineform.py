from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

# Form fill to write a line of the roast
class LineForm(FlaskForm):
    lines = TextAreaField('Your lines.', validators=[DataRequired()], render_kw={'id': 'lines'})
    sbutton = SubmitField('Go!', render_kw={'id': 'sbutton'})
    cbutton = SubmitField('Start over.', render_kw={'id': 'cbutton'})
