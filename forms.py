from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email
from models import db, User, Task

class LoginForm(Form):
    username = StringField("Username", validators=[validators.DataRequired(message="Please Fill This Field")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])

class RegisterForm(Form):
    firstname = StringField("Firstname", validators=[validators.Length(min=3, max=30),
                            validators.DataRequired(message="Please Fill This Field")])
    lastname = StringField("Lastname", validators=[validators.Length(min=3, max=30),
                            validators.DataRequired(message="Please Fill This Field")])
    username = StringField("Username", validators=[validators.Length(min=3, max=15),
                            validators.DataRequired(message="Please Fill This Field")])
    email = StringField("Email", validators=[validators.Length(min=11, max=50),
                            validators.DataRequired(message="Please enter a valid email address"),
                            Email(message="Please enter a valid email address")])
    password = PasswordField("Password", validators=[validators.Length(min=8, max=30),
                            validators.DataRequired(message="Please Fill This Field"),
                            validators.EqualTo(fieldname="confirm_password", message="Your Passwords Do Not Match")])
    confirm_password = PasswordField("Confirm Password", validators=[validators.Length(min=8, max=30),
                            validators.DataRequired(message="Please Fill This Field")])
    gender = RadioField("Gender", choices=[("Male", "Male"),("Female", "Female")])

    def validate_username(self, username):
        user = db.session.query(User).filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.query(User).filter(User.email == email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class TaskForm(Form):
    name = StringField("Task Name", validators=[validators.Length(min=3, max=30),
                            validators.DataRequired(message="Please Fill This Field")])
    file_path = StringField("File Path", validators=[validators.DataRequired(message="Please Fill This Field")])
    step = IntegerField("Prediction Step", validators=[validators.DataRequired(message="Please Fill This Field")])

    def validate_taskname(self, name):
        task = db.session.query(Task).filter(Task.name == name.data).first()
        if task is not None:
            raise ValidationError('Task is already in the system. Please use a different name.')