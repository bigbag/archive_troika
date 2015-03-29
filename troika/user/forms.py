from flask_wtf import Form
from wtforms import PasswordField, TextField
from wtforms.validators import DataRequired, Email, Length

from .models import User


class LoginForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(email=self.email.data).first()
        if not self.user or not self.user.check_password(self.password.data):
            self.email.errors.append('User not found')
            self.password.errors.append('Invalid password')
            return False

        if self.user.status != User.STATUS_ACTIVE:
            self.email.errors.append('User not activated')
            return False
        return True
