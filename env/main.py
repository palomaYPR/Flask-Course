from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest

app = Flask(__name__, template_folder='../templates', static_folder='../static')
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SECRET'
# app.config['WTF_CSRF_ENABLED']= False

todos = ['Comprar café', 'Enviar solicitud de compra', 'Finalizar proyecto']


class LoginForm(Form):
    username = StringField('Nombre de usuario: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Enviar')


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_crasher(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    user_ip = session.get('user_ip')
    login_form = LoginForm(request.form)
    username = session.get('username')

    contexto = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }

    # if login_form.validate_on_submit():

    if request.method == "POST" and login_form.validate():
        username = login_form.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))

    return render_template('hello.html', **contexto)
