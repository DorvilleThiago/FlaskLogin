from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, LoginManager

def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print("Database created!")


app = Flask(__name__)

db = SQLAlchemy()
DB_NAME = "database.db"
app.config['SECRET_KEY'] = 'bestkeyever'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
        return models.User.query.get(int(id))

import models

create_database(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = u"Você precisa fazer login para acessar esta página."
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
        return models.User.query.get(int(id))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login realizado com sucesso!', category='success')
                login_user(user, remember=True) 
                return redirect(url_for('index'))
            else:
                flash('Senha incorreta, tente novamente...', category='error')
        else:
            flash('Este email não está registrado no banco de dados', category='error')

    return render_template("login.html")

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        senha1 = request.form.get('password1')
        senha2 = request.form.get('password2')

        user = models.User.query.filter_by(email=email).first()
        if user:
            flash('Esse email já possui uma conta neste website', category='error')
        elif len(email) < 4:
            flash('Seu email é inválido, tente novamente.', category='error')
        elif len(senha1) < 8:
            flash('Sua senha deve conter pelo menos 8 caracteres.', category='error')
        elif senha1 < senha2:
            flash('Sua senhas que você digitou não são iguais.', category='error')
        else:
            new_user = models.User(email=email,password=generate_password_hash(senha1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Conta registrada, obrigado!',category='success')
            login_user(user, remember=True)
            return redirect(url_for('index'))

    return render_template("register.html")

@app.route("/<string:nome>")
def Erro404(nome):
    variavel = f"ERRO, página {nome} não existe."
    return render_template("erro.html", name=variavel)

if __name__ == '__main__':
    app.run(debug=True)
