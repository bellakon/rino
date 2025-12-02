"""
Feature: Autenticación
Sistema de login básico para proteger el acceso al sistema
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from app.config.users_config import USERS, SESSION_LIFETIME_SECONDS
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


def login_required(f):
    """
    Decorador para proteger rutas que requieren autenticación
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Debe iniciar sesión para acceder', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        # Verificar si la sesión ha expirado
        login_time = session.get('login_time')
        if login_time:
            login_dt = datetime.fromisoformat(login_time)
            if datetime.now() - login_dt > timedelta(seconds=SESSION_LIFETIME_SECONDS):
                session.clear()
                flash('Su sesión ha expirado. Por favor inicie sesión nuevamente.', 'warning')
                return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    # Si ya está logueado, redirigir al home
    if session.get('logged_in'):
        return redirect(url_for('home'))
    
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validar credenciales
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            session['login_time'] = datetime.now().isoformat()
            session.permanent = True
            
            flash(f'Bienvenido, {username}!', 'success')
            
            # Redirigir a la página solicitada o al home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            error = 'Usuario o contraseña incorrectos'
    
    return render_template('auth/login.html', error=error)


@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    username = session.get('username', 'Usuario')
    session.clear()
    flash(f'Sesión cerrada. Hasta pronto, {username}!', 'info')
    return redirect(url_for('auth.login'))
