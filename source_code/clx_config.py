from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, IPAddress

class ConfigForm(FlaskForm):
    ip_address = StringField("IP Address", validators=[DataRequired(), IPAddress(ipv4=True, ipv6=False, message=None)])
    user_name = StringField("User name", validators=[DataRequired()])
    user_pass = PasswordField("User pass", validators=[DataRequired(), Length(min=4, max=15)])
    user_pin = StringField("User PIN", validators=[DataRequired(), Length(min=4, max=4)])
    data_file = FileField("CSV file", validators=[DataRequired()])
    comment = StringField("Comment", validators=[DataRequired()])
