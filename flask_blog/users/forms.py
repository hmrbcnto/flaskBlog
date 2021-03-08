

#RegistrationForm class
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        #Check if there is an entry with matching username in database
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken.')

    def validate_email(self, email):
        #Check if there is an entry with matching email in database
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken.')



#LoginForm class
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#Update Account form
class UpdateForm(FlaskForm):
    username = StringField('New Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('New Email',
                        validators=[DataRequired(), Email()])
    profilePicture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            #Check if there is an entry with matching username in database
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            #Check if there is an entry with matching email in database
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken.')

#Reset Password Form: Submit Email
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        #Check if there is an entry with matching email in database
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email is not registered.')

#Reset Password Form: New Password
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
