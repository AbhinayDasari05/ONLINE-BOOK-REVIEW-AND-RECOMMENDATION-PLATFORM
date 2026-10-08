from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.services.user_service import UserService
from app.core.audit import log_audit_event

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint (REQ-01)."""
    if current_user.is_authenticated:
        return redirect(url_for('catalog.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('auth/login_register.html', active_tab='register', username=username, email=email)

        success, message, user = UserService.register_user(username, email, password)
        if success:
            flash("Registration successful! You may now log in.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash(message, "danger")
            return render_template('auth/login_register.html', active_tab='register', username=username, email=email)

    return render_template('auth/login_register.html', active_tab='register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User authentication endpoint (REQ-02)."""
    if current_user.is_authenticated:
        return redirect(url_for('catalog.index'))

    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        success, message, user = UserService.authenticate_user(username_or_email, password)
        if success and user:
            login_user(user, remember=remember)
            flash(f"Welcome back, {user.username}!", "success")
            next_page = request.args.get('next')
            # Protect against open redirect
            if not next_page or not next_page.startswith('/') or next_page.startswith('//'):
                next_page = url_for('catalog.index')
            return redirect(next_page)
        else:
            flash(message, "danger")

    return render_template('auth/login_register.html', active_tab='login')

@auth_bp.route('/logout')
@login_required
def logout():
    """Server-side session invalidation and logout (REQ-12, CTRL-01)."""
    username = current_user.username
    user_id = current_user.id
    logout_user()
    session.clear()  # Server-side invalidation
    log_audit_event("LOGOUT", "User", user_id, "SUCCESS", f"User {username} logged out")
    flash("You have been securely logged out.", "info")
    return redirect(url_for('auth.login'))
