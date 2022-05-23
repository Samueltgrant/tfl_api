from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FieldList
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class JourneyDetailsForm(FlaskForm):
    user = StringField('User', validators=[], render_kw={"placeholder": "User 1"})
    station = StringField('Station', id='station', validators=[DataRequired()])
    submit = SubmitField('Search')
