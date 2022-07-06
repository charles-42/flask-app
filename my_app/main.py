from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .utils import admin_required
import requests

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    first_name = current_user.name
    if not current_user.name:
        return render_template('admin_profile.html', name=current_user.name,age = 'young') 
    api_result = requests.get('https://api.agify.io/?name=' + first_name)
    return render_template('profile.html', name=current_user.name, age = api_result.json()['age'])

@main.route('/admin', methods=['GET'])
@login_required
@admin_required
def admin_page():
    first_name = current_user.name
    if not current_user.name:
        return render_template('admin_profile.html', name=current_user.name,age = 'young') 
    api_result = requests.get('https://api.agify.io/?name=' + first_name)
    return render_template('admin_profile.html', name=current_user.name,age = api_result.json()['age'])