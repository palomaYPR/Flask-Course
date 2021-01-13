from flask import render_template, session, redirect, flash, url_for, request 
from app.forms import LoginForm
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    context = {
        'login_form': login_form
    }

    if request.method == "POST" and login_form.validate():
        username = login_form.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))

    return render_template('login.html', **context)
