from presto import app
from presto.database import db_session
from presto.models import User
from presto.forms import UserForm
from flask import request, render_template, redirect
from sqlalchemy.exc import IntegrityError


@app.route('/admin/users')
def manage_users():
    users = User.query.all()

    return render_template('manage_users.html', users=enumerate(users, start=1))


@app.route('/admin/users/add', methods=['POST', 'GET'])
def add_user():
    form = UserForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User(login=form.login.data,
                    mail=form.mail.data,
                    password=form.password.data)

        try:
            db_session.add(user)
            db_session.commit()
            return redirect('/admin/users', 303)
        except IntegrityError:
            form.login.errors.append('Login lub mail jest już używany')
            db_session.rollback()

    return render_template('user.html', form=form)
