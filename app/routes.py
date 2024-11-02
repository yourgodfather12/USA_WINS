from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from . import db
from .models import Image
import os
import time

# Define Blueprint for routes
bp = Blueprint('main', __name__)

# Define allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/map')
@login_required
def map():
    return render_template('map.html')

@bp.route('/county/<county_id>')
@login_required
def county(county_id):
    # Fetch images related to a specific county
    images = Image.query.filter_by(location=county_id).all()
    return render_template('county.html', images=images, county_id=county_id)

@bp.route('/upload', methods=['POST'])
@login_required
def upload_image():
    # Check if a file is part of the POST request
    if 'file' not in request.files:
        flash('No file selected.')
        return redirect(request.url)

    file = request.files['file']
    location = request.form.get('location')

    # Check if file is allowed and has a secure filename
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        unique_filename = f"{timestamp}_{filename}"
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')  # default 'uploads' if config is missing
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, unique_filename)

        try:
            # Save file and add record to the database
            file.save(file_path)
            new_image = Image(filename=unique_filename, location=location)
            db.session.add(new_image)
            db.session.commit()
            flash('File successfully uploaded.')
        except Exception as e:
            # Rollback if any issue occurs
            db.session.rollback()
            flash(f'Failed to upload file: {str(e)}')
    else:
        flash('Invalid file type.')

    return redirect(url_for('main.county', county_id=location))

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/faq')
def faq():
    return render_template('faq.html')

@bp.route('/states')
@login_required
def states():
    return render_template('states.html')
