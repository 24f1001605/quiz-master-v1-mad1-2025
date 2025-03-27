from flask import render_template, request, flash, redirect, url_for
from app import app, db
from models import User, Question, Quiz, Subject, Chapter, Scores
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        fullname = request.form['fullname']
        qualification = request.form['qualification']
        dob_str = request.form['dob'] 

        if not all([username, password, confirm_password, fullname, qualification, dob_str]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            
            new_user = User(
                username=username,
                password=generate_password_hash(password),
                fullname=fullname,
                qualification=qualification,
                dob=dob
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')
