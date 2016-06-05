from flask import redirect, render_template, request, url_for
from presto import app
from presto.database import db_session
from presto.forms import UserForm, EditUserForm, ShippingTypesForm
from presto.models import User, ShippingType
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
            return redirect(url_for('manage_users'))
        except IntegrityError:
            db_session.rollback()
            form.login.errors.append('Login lub mail jest już używany')

    return render_template('user.html', form=form)


@app.route('/admin/users/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return render_template('errors/404.html'), 404

    db_session.delete(user)
    db_session.commit()

    return redirect(url_for('manage_users'))


@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return render_template('errors/404.html'), 404

    form = EditUserForm(request.form)

    if request.method == 'POST' and form.validate():
        user.login = form.login.data
        user.mail = form.mail.data

        try:
            db_session.add(user)
            db_session.commit()
            return redirect(url_for('manage_users'))
        except IntegrityError:
            db_session.rollback()
            form.login.errors.append('Login lub mail jest już używany')

    return render_template('edit_user.html', form=form, user=user)


@app.route('/admin/shipping/types')
def manage_shipping_types():
    shipping_types = ShippingType.query.all()
    return render_template('shipping_types.html', shipping_types=enumerate(shipping_types, 1))

@app.route('/admin/shipping/types/add')
def add_shipping_type():
    pass


@app.route('/admin/shipping/types/edit/<int:shipping_type_id>')
def edit_shipping_type(shipping_type_id):
    pass


@app.route('/admin/shipping/types/delete/<int:shipping_type_id>')
def delete_shipping_type(shipping_type_id):
    pass
