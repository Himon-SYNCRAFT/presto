"""
Views for admin panel. Mostly CRUD.
"""

from flask import Blueprint, redirect, render_template, request, url_for, flash
from presto.database import db_session
from presto.forms import UserForm, EditUserForm, ShippingTypesForm,\
    AuctionTypesForm, RolesForm
from presto.models import User, ShippingType, AuctionType, Role
from sqlalchemy.exc import IntegrityError


admin = Blueprint('admin', __name__, template_folder='templates',
                  url_prefix='/admin')


@admin.route('/users')
def manage_users():
    users = User.query.all()

    return render_template('admin/users/list.html', users=enumerate(users, start=1))


@admin.route('/users/add', methods=['POST', 'GET'])
def add_user():
    form = UserForm(request.form)
    form.role.choices = [(role.id, role.name)
                         for role in Role.query.order_by('name')]

    if request.method == 'POST' and form.validate():
        user = User(login=form.login.data,
                    mail=form.mail.data,
                    password=form.password.data,
                    role_id=form.role.data)

        try:
            db_session.add(user)
            db_session.commit()
            return redirect(url_for('admin.manage_users'))
        except IntegrityError:
            db_session.rollback()
            form.login.errors.append('Login lub mail jest już używany')

    return render_template('admin/users/add.html', form=form)


@admin.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return render_template('admin/errors/404.html'), 404

    db_session.delete(user)
    db_session.commit()

    return redirect(url_for('admin.manage_users'))


@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return render_template('admin/errors/404.html'), 404

    form = EditUserForm(request.form)
    form.role.choices = [(role.id, role.name)
                         for role in Role.query.order_by('name')]
    form.role.default = user.role_id
    form.process(request.form)

    if request.method == 'POST' and form.validate():
        user.login = form.login.data
        user.mail = form.mail.data

        try:
            db_session.add(user)
            db_session.commit()
            return redirect(url_for('admin.manage_users'))
        except IntegrityError:
            db_session.rollback()
            form.login.errors.append('Login lub mail jest już używany')

    return render_template('admin/users/form.html', form=form, user=user)


@admin.route('/shipping/types')
def manage_shipping_types():
    shipping_types = ShippingType.query.all()
    return render_template('admin/shipping_types/list.html', shipping_types=enumerate(shipping_types, 1))


@admin.route('/shipping/types/add', methods=['GET', 'POST'])
def add_shipping_type():
    form = ShippingTypesForm(request.form)

    if request.method == 'POST' and form.validate():
        shipping_type = ShippingType(name=form.name.data,
                                     is_boolean=form.is_boolean.data)

        db_session.add(shipping_type)

        try:
            db_session.commit()
            return redirect(url_for('admin.manage_shipping_types'))
        except IntegrityError:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('admin/shipping_types/form.html', form=form)


@admin.route('/shipping/types/edit/<int:shipping_type_id>', methods=['GET', 'POST'])
def edit_shipping_type(shipping_type_id):
    shipping_type = ShippingType.query.filter_by(id=shipping_type_id).first()

    if shipping_type is None:
        return render_template('admin/errors/404.html'), 404

    form = ShippingTypesForm(request.form)

    if request.method == 'POST' and form.validate():
        shipping_type.name = form.name.data
        shipping_type.is_boolean = form.is_boolean.data

        db_session.add(shipping_type)

        try:
            db_session.commit()
            return redirect(url_for('admin.manage_shipping_types'))
        except IntegrityError as ex:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('admin/shipping_types/form.html', form=form, shipping_type=shipping_type)


@admin.route('/shipping/types/delete/<int:shipping_type_id>')
def delete_shipping_type(shipping_type_id):
    shipping_type = ShippingType.query.filter_by(id=shipping_type_id).first()

    if shipping_type is None:
        return render_template('admin/errors/404.html'), 404

    db_session.delete(shipping_type)
    db_session.commit()

    return redirect(url_for('admin.manage_shipping_types'))


@admin.route('/auction/types')
def manage_auction_types():
    auction_types = AuctionType.query.all()

    return render_template('admin/auction_types/list.html', auction_types=enumerate(auction_types, 1))


@admin.route('/auction/types/add', methods=['GET', 'POST'])
def add_auction_type():
    form = AuctionTypesForm(request.form)

    if request.method == 'POST' and form.validate():
        auction_type = AuctionType(name=form.name.data)
        db_session.add(auction_type)

        try:
            db_session.commit()
            return redirect(url_for('admin.manage_auction_types'))
        except IntegrityError:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('admin/auction_types/form.html', form=form)


@admin.route('/auction/types/edit/<int:auction_type_id>', methods=['GET', 'POST'])
def edit_auction_type(auction_type_id):
    auction_type = AuctionType.query.filter_by(id=auction_type_id).first()

    if auction_type is None:
        return render_template('admin/errors/404.html'), 404

    form = AuctionTypesForm(request.form)

    if request.method == 'POST' and form.validate():
        auction_type.name = form.name.data
        db_session.add(auction_type)

        try:
            db_session.commit()
            return redirect(url_for('admin.manage_auction_types'))
        except IntegrityError:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('admin/auction_types/form.html', form=form, auction_type=auction_type)


@admin.route('/auction/types/delete/<int:auction_type_id>', methods=['GET'])
def delete_auction_type(auction_type_id):
    auction_type = AuctionType.query.filter_by(id=auction_type_id).first()

    if auction_type is None:
        return render_template('admin/errors/404.html'), 404

    db_session.delete(auction_type)
    db_session.commit()

    return redirect(url_for('admin.manage_auction_types'))


@admin.route('/users/roles')
def manage_roles():
    roles = Role.query.all()

    return render_template('admin/roles/list.html', roles=enumerate(roles, 1))


@admin.route('/users/roles/add', methods=['GET', 'POST'])
def add_role():
    form = RolesForm(request.form)

    if request.method == 'POST' and form.validate():
        role = Role(name=form.name.data)
        db_session.add(role)

        try:
            db_session.commit()
            return redirect(url_for('admin.manage_roles'))
        except IntegrityError:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('admin/roles/form.html', form=form)


@admin.route('/users/roles/edit/<int:role_id>', methods=['GET', 'POST'])
def edit_role(role_id):
    role = Role.query.filter_by(id=role_id).first()

    if role is None:
        return render_template('admin/errors/404.html'), 404

    form = RolesForm(request.form)

    if request.method == 'POST' and form.validate():
        role.name = form.name.data
        db_session.add(role)

        try:
            db_session.commit()
            return redirect(url_for('admin.manage_roles'))
        except IntegrityError:
            db_session.rollback()
            form.name.errors.append('Nazwa jest już zajęta')

    return render_template('admin/roles/form.html', form=form, role=role)


@admin.route('/users/roles/delete/<int:role_id>')
def delete_role(role_id):
    role = Role.query.filter_by(id=role_id).first()

    if role is None:
        return render_template('admin/errors/404.html'), 404

    db_session.delete(role)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        flash('Nie można usunąć roli, gdy istnieją przypisanie do niej użytkownicy')

    return redirect(url_for('admin.manage_roles'))
