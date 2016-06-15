from wtforms import Form, StringField, PasswordField, SubmitField, \
    BooleanField
from wtforms.validators import InputRequired, Length, Email


class UserForm(Form):
    login = StringField(
        'Login',
        [InputRequired(message='Pole login jest polem wymaganym'),
         Length(min=5, max=128, message='Login musi mieć min 5 znaków i max 128')]
    )

    mail = StringField(
        'Mail',
        [InputRequired(message='Pole mail jest polem wymaganym'),
         Email(message='Niepoprawny format email')]
    )

    password = PasswordField('Hasło', [InputRequired(
        message='Pole hasło jest polem wymaganym')])

    submit = SubmitField('Zapisz')


class EditUserForm(Form):
    login = StringField(
        'Login',
        [InputRequired(message='Pole login jest polem wymaganym'),
         Length(min=5, max=128, message='Login musi mieć min 5 znaków i max 128')]
    )

    mail = StringField(
        'Mail', [InputRequired(message='Pole mail jest polem wymaganym'),
                 Email(message='Niepoprawny format email')])
    submit = SubmitField('Zapisz')


class ShippingTypesForm(Form):
    name = StringField(
        'Nazwa',
        [InputRequired('Pole nazwa jest wymagane'),
         Length(max=128, message='Nazwa musi mieć max 128 znaków')]
    )

    is_boolean = BooleanField('Wartość boolowska')
    submit = SubmitField('Zapisz')

class AuctionTypesForm(Form):
    name = StringField(
        'Nazwa',
        [InputRequired('Pole nazwa jest wymagane'),
         Length(max=128, message='Nazwa musi mieć max 128 znaków')]
    )

    submit = SubmitField('Zapisz')
