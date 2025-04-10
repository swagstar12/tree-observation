from flask import Flask, render_template, redirect, url_for, request, flash, session, Response, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Tree, Question, Submission, Answer
from datetime import date
import csv
from io import StringIO
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create DB on first request
#@app.before_first_request
#def create_db_if_not_exists():
#    db_path = '/tmp/tree.db'
#    if not os.path.exists(db_path):
#        db.create_all()

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Try a different one.', 'warning')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    trees = Tree.query.all()
    return render_template('dashboard.html', trees=trees)

@app.route('/observe/<int:tree_id>', methods=['GET', 'POST'])
@login_required
def observe(tree_id):
    existing_submission = Submission.query.filter_by(
        user_id=current_user.id,
        tree_id=tree_id,
        submission_date=date.today()
    ).first()

    if existing_submission:
        flash("You've already submitted today's observation for this tree.", 'info')
        return redirect(url_for('dashboard'))

    questions = Question.query.filter_by(tree_id=tree_id).all()

    if request.method == 'POST':
        submission = Submission(user_id=current_user.id, tree_id=tree_id, submission_date=date.today())
        db.session.add(submission)
        db.session.commit()

        for question in questions:
            selected_option = request.form.get(str(question.id))
            if selected_option:
                answer = Answer(
                    submission_id=submission.id,
                    question_id=question.id,
                    selected_option=selected_option
                )
                db.session.add(answer)

        db.session.commit()
        flash('Observation submitted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('questionnaire.html', questions=questions, tree_id=tree_id)

@app.route('/submissions')
@login_required
def view_submissions():
    submissions = Submission.query.filter_by(user_id=current_user.id).order_by(Submission.submission_date.desc()).all()
    return render_template('submissions.html', submissions=submissions)

@app.route('/export_csv')
@login_required
def export_csv():
    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(['Username', 'Tree Name', 'Submission Date', 'Question', 'Selected Option'])

    submissions = Submission.query.all()

    for submission in submissions:
        user = User.query.get(submission.user_id)
        tree = Tree.query.get(submission.tree_id)
        answers = Answer.query.filter_by(submission_id=submission.id).all()
        for answer in answers:
            question = Question.query.get(answer.question_id)
            writer.writerow([
                user.username,
                tree.name,
                submission.submission_date.strftime('%Y-%m-%d'),
                question.question_text,
                answer.selected_option
            ])

    output.seek(0)
    return Response(output, mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=submissions.csv"})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("No account found with that username.", "danger")
            return redirect(url_for('reset_password'))

        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Password updated successfully! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('reset_password.html')

@app.route('/init_db')
def init_db():
    db.create_all()
    return "Database initialized!"



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Only run locally!
    app.run()

