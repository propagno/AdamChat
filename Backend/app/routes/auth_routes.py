from flask import Blueprint, Flask, request, render_template, redirect, url_for, session
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
auth_controller = AuthController()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object('app.config.Config')


@app.route('/')
def home():
    return render_template('login.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        result = auth_controller.login(email, password)
        if result.get('status') == 'success':
            session['user_email'] = email
            return redirect(url_for('dashboard_bp.dashboard'))
        else:
            return render_template('login.html', error=result.get('message'))
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        result = auth_controller.register(email, password)
        if result.get('status') == 'success':
            return redirect(url_for('auth_bp.confirm'))
        else:
            return render_template('register.html', error=result.get('message'))
    return render_template('register.html')


@auth_bp.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        email = request.form.get('email')
        confirmation_code = request.form.get('confirmation_code')
        result = auth_controller.confirm(email, confirmation_code)
        if 'error' not in result:
            return redirect(url_for('auth_bp.login'))
        else:
            return render_template('confirm.html', error=result.get('error'))
    return render_template('confirm.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_bp.login'))


app.register_blueprint(auth_bp)
