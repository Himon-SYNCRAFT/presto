from flask import redirect, render_template, request, url_for
from presto import app
from presto.database import db_session
from presto.forms import UserForm, EditUserForm, ShippingTypesForm,\
    AuctionTypesForm, RolesForm
from presto.models import User, ShippingType, AuctionType, Role
from sqlalchemy.exc import IntegrityError


@app.route('/admin/users')
def manage_users():
    users = User.query.all()

    return render_template('manage_users.html', users=enumerate(users, start=1))


@app.route('/admin/users/add', methods=['POST', 'GET'])
def add_user():
    form = UserForm(request.form)
    form.role.choices = [(role.id, role.name) for role in Role.query.order_by('name')]

    if request.method == 'POST' and form.validate():
        user = User(login=form.login.data,
                    mail=form.mail.data,
                    password=form.password.data,
                    role_id=form.role.data)

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
    form.role.choices = [(role.id, role.name) for role in Role.query.order_by('name')]
    form.role.default = user.role_id
    form.process(request.form)

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


@app.route('/admin/shipping/types/add', methods=['GET', 'POST'])
def add_shipping_type():
    form = ShippingTypesForm(request.form)

    if request.method == 'POST' and form.validate():
        shipping_type = ShippingType(name=form.name.data,
                                     is_boolean=form.is_boolean.data)

        db_session.add(shipping_type)

        try:
            db_session.commit()
            return redirect(url_for('manage_shipping_types'))
        except IntegrityError:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('shipping_types_add.html', form=form)


@app.route('/admin/shipping/types/edit/<int:shipping_type_id>', methods=['GET', 'POST'])
def edit_shipping_type(shipping_type_id):
    shipping_type = ShippingType.query.filter_by(id=shipping_type_id).first()

    if shipping_type is None:
        return render_template('errors/404.html'), 404

    form = ShippingTypesForm(request.form)

    if request.method == 'POST' and form.validate():
        shipping_type.name = form.name.data
        shipping_type.is_boolean = form.is_boolean.data

        db_session.add(shipping_type)

        try:
            db_session.commit()
            return redirect(url_for('manage_shipping_types'))
        except IntegrityError as ex:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('shipping_types_edit.html', form=form, shipping_type=shipping_type)


@app.route('/admin/shipping/types/delete/<int:shipping_type_id>')
def delete_shipping_type(shipping_type_id):
    shipping_type = ShippingType.query.filter_by(id=shipping_type_id).first()

    if shipping_type is None:
        return render_template('errors/404.html'), 404

    db_session.delete(shipping_type)
    db_session.commit()

    return redirect(url_for('manage_shipping_types'))


@app.route('/admin/auction/types')
def manage_auction_types():
    auction_types = AuctionType.query.all()

    return render_template('auction_types.html', auction_types=enumerate(auction_types, 1))


@app.route('/admin/auction/types/add', methods=['GET', 'POST'])
def add_auction_type():
    form = AuctionTypesForm(request.form)

    if request.method == 'POST' and form.validate():
        auction_type = AuctionType(name=form.name.data)
        db_session.add(auction_type)

        try:
            db_session.commit()
            return redirect(url_for('manage_auction_types'))
        except IntegrityError:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('auction_types_add.html', form=form)


@app.route('/admin/auction/types/edit/<int:auction_type_id>', methods=['GET', 'POST'])
def edit_auction_type(auction_type_id):
    auction_type = AuctionType.query.filter_by(id=auction_type_id).first()

    if auction_type is None:
        return render_template('errors/404.html'), 404

    form = AuctionTypesForm(request.form)

    if request.method == 'POST' and form.validate():
        auction_type.name = form.name.data
        db_session.add(auction_type)

        try:
            db_session.commit()
            return redirect(url_for('manage_auction_types'))
        except IntegrityError:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('auction_types_edit.html', form=form, auction_type=auction_type)


@app.route('/admin/auction/types/delete/<int:auction_type_id>', methods=['GET'])
def delete_auction_type(auction_type_id):
    auction_type = AuctionType.query.filter_by(id=auction_type_id).first()

    if auction_type is None:
        return render_template('errors/404.html'), 404

    db_session.delete(auction_type)
    db_session.commit()

    return redirect(url_for('manage_auction_types'))


@app.route('/admin/users/roles')
def manage_roles():
    roles = Role.query.all()

    return render_template('roles.html', roles=enumerate(roles, 1))

@app.route('/admin/users/roles/add', methods=['GET', 'POST'])
def add_role():
    form = RolesForm(request.form)

    if request.method == 'POST' and form.validate():
        role = Role(name=form.name.data)
        db_session.add(role)

        try:
            db_session.commit()
            return redirect(url_for('manage_roles'))
        except IntegrityError:
            db_session.rollback()
            form.name.error.append('Nazwa jest już zajęta')

    return render_template('role_add.html', form=form)
