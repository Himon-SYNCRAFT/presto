from wtforms import Form, StringField, PasswordField, SubmitField, validators, \
    BooleanField


class UserForm(Form):
    login = StringField('Login', [validators.InputRequired(message='Pole login jest polem wymaganym'),
                                  validators.Length(min=5, max=128, message='Login musi mieć min 5 znaków i max 128')])
    mail = StringField('Mail', [validators.InputRequired(message='Pole mail jest polem wymaganym'),
                                validators.Email(message='Niepoprawny format email')])
    password = PasswordField('Hasło', [validators.InputRequired(
        message='Pole hasło jest polem wymaganym')])
    submit = SubmitField('Zapisz')


class EditUserForm(Form):
    login = StringField('Login', [validators.InputRequired(message='Pole login jest polem wymaganym'),
                                  validators.Length(min=5, max=128, message='Login musi mieć min 5 znaków i max 128')])
    mail = StringField('Mail', [validators.InputRequired(message='Pole mail jest polem wymaganym'),
                                validators.Email(message='Niepoprawny format email')])
    submit = SubmitField('Zapisz')

class ShippingTypesForm(Form):
    name = StringField('Nazwa', [validators.InputRequired('Pole nazwa jest wymagane')])
    is_boolean = BooleanField('Wartość boolowska')
    submit = SubmitField('Zapisz')
