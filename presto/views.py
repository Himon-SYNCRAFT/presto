from presto import app
from presto.models import User
from presto.forms import UserForm
from flask import request, render_template


@app.route('/')
def index():
    form = UserForm(request.form)

    return render_template('user.html', form=form)

@app.route('/admin/users')
def manage_users():
    users = User.query.all()

    return render_template('manage_users.html', users=enumerate(users, start=1))
