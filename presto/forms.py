from wtforms import Form, StringField, PasswordField, SubmitField, validators


class UserForm(Form):
    login = StringField('Login', [validators.InputRequired(message='Pole login jest polem wymaganym'),
                                  validators.Length(min=6, max=128, message='Login musi mieć min 6 znaków i max 128')])
    mail = StringField('Mail', [validators.InputRequired(message='Pole mail jest polem wymaganym'),
                                validators.Email(message='Niepoprawny format email')])
    password = PasswordField('Hasło', [validators.InputRequired(
        message='Pole hasło jest polem wymaganym')])
    submit = SubmitField('Zapisz')
