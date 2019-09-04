from  flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, SelectField, validators, PasswordField 
from wtforms.fields.html5 import DateField

class saveForm(FlaskForm):
    id = TextField('ID', [validators.Required()])
    name = TextField('Name', [validators.Required()])
    dob = DateField('Date of Birth', [validators.Required()], format="%Y-%m-%d")
    rank = SelectField('Rank',
            choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Developer', 'Developer')])
    address = TextAreaField('Address', [validators.Required('Enter Address')])

class registerForm(FlaskForm):
        username = TextField("Username", [validators.Required()])
        email = TextField("Email",[validators.Required()])
        password = PasswordField("Password",[validators.Required()])

class loginForm(FlaskForm):
        username = TextField("Username", [validators.Required()])
        password = PasswordField("Password", [validators.Required()])