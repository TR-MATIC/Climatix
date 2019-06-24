from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, IPAddress

class ConfigForm(FlaskForm):
    addr = StringField("IP Address", validators=[DataRequired(), IPAddress(ipv4=True, ipv6=False, message=None)])
    name = StringField("User name", validators=[DataRequired()])
    pasw = PasswordField("User pass", validators=[DataRequired(), Length(min=4, max=20)])
    pin = StringField("User PIN", validators=[DataRequired(), Length(min=4, max=4)])
    path = FileField("CSV file", validators=[DataRequired()])
    comt = StringField("Comment", validators=[DataRequired()])
