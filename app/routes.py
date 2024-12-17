import logging
from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Post
from .extensions import db, bcrypt

# Configure o logger
logging.basicConfig(level=logging.DEBUG)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return redirect('/feed' if current_user.is_authenticated else '/login')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já existe. Por favor, escolha outro.')
            return render_template('register.html')
        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect('/feed')
        except Exception as e:
            db.session.rollback()
            logging.error('Erro ao criar o usuário: %s', e)
            flash('Erro ao criar o usuário: {}'.format(e))
            return render_template('register.html')
    return render_template('register.html')

@main_bp.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    if request.method == 'POST':
        body = request.form['body']
        new_post = Post(body=body, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/feed')
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/feed')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/feed')
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')
