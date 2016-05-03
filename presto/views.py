from presto import app
from presto.forms import UserForm
from flask import request, render_template


@app.route('/')
def index():
    form = UserForm(request.form)

    return render_template('user.html', form=form)
