from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .utils import admin_required
from . import db


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/admin', methods=['GET'])
@login_required
@admin_required
def admin_page():
    return render_template('profile.html', name=current_user.name)