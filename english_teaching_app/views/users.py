#!/usr/bin/python3
from flask import Blueprint,session,render_template,request,url_for,redirect,flash
from models.user import User, UserErrors, requires_admin,requires_login

user_blueprint = Blueprint('users',__name__)

@user_blueprint.route('/register',methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        try:
            User.register_user(email,password,firstname,lastname)
            session['email'] = email
            return redirect(url_for('lessons.index'))
        except UserErrors.UserError as e:
            flash(e.message,'danger')

    return render_template('users/register.html')

@user_blueprint.route('/login', methods=['GET','POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        next_url = request.form.get("next")

        try:
            if User.is_login_valid(email,password):
                session['email'] = email
                #flash('It\'s really you! Welcome!','success')
                if next_url:
                    return redirect(next_url)
                return redirect(url_for('lessons.index'))

        except UserErrors.UserError as e:
            flash(e.message,'danger')

    return render_template('users/login.html')

@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('.login_user'))
