from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_migrate import Migrate
from models import db, Task, User, Login
from forms import LoginForm, RegisterForm, TaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:veletibine07@localhost:5432/pizza_sales_v2'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def task_page():
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks/<int:id>', methods=['GET'])
def task_by_id(id):
    task = db.session.query(Task).filter(Task.id == id).first()
    if task:
        tbi = task
        return render_template('tasks.html', tbi=tbi)

    flash('Task not found.', 'danger')
    return redirect('/')

@app.route('/create_task/', methods=['GET', 'POST'])
def create_task():
    form = TaskForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        started = 'N/A'
        finished = 'N/A'
        status = 'Not Started'
        file_path = form.file_path.data
        step = form.step.data
        result = 'N/A'
        new_task = Task(name=name, started=started, finished=finished, status=status,
                        step=step, file_path=file_path, result=result)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            flash('There was an issue adding your task.', 'danger')
            return redirect('/create_task')

    return render_template('task.html', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        gender = form.gender.data
        register_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user = User(firstname=firstname, lastname=lastname, username=username, email=email,
                        password=password, gender=gender, register_date=register_date)

        try:
            db.session.add(new_user)
            db.session.commit()
            session['username'] = form.username.data
            return redirect('/login')
        except:
            flash('There was an issue while registering.', 'danger')
            return redirect('/register')

    return render_template('register.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        user = db.session.query(User).filter(User.username == username).first()

        if user:
            if check_password_hash(user.password, password):
                session['username'] = user.username
                user.authenticated = True
                new_login = Login(username=username, password=generate_password_hash(password), authenticated=user.authenticated)
                db.session.add(new_login)
                db.session.commit()
                flash('Welcome ' + user.firstname + '!', 'info')
                return redirect(url_for('profile', username=user.username))
            else:
                flash('Username or Password Incorrect.', 'danger')
                return redirect('/login')
        else:
            flash('User not found!', 'danger')
            return redirect('/register')

    return render_template('login.html', form=form)

@app.route('/logout/', methods=['GET'])
def logout():
    user = db.session.query(Login).filter(Login.authenticated == True).first()
    if user:
        user.authenticated = False
        db.session.commit()
        session.clear()
        return redirect('/')
    else:
        flash('You are already logged out!', 'danger')
        return redirect('/login')

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user:
        return render_template('profile.html', user=user)

    flash('Profile not found.', 'danger')
    return redirect('/')

@app.route('/predict/<int:id>', methods=['GET'])
def predict(id):
    task = db.session.query(Task).filter(Task.id == id).first()
    file_name = task.file_path
    step = task.step

    started_time = dt.now().time().strftime("%H:%M:%S")

    df = pd.read_excel(file_name, engine='openpyxl')
    categories = df["CATEGORY"].unique()
    result = {}

    for category in categories:
        pizza = df.loc[df["CATEGORY"] == category]

        cols = ['CATEGORY']
        pizza.drop(cols, axis=1, inplace=True)
        pizza = pizza.sort_values("DATE")
        pizza = pizza.groupby('DATE')['SALES'].sum().reset_index()

        pizza = pizza.set_index('DATE')
        ts = pizza["SALES"].resample("MS").mean()

        mod = sm.tsa.statespace.SARIMAX(ts, order=(1, 1, 1), seasonal_order=(1, 1, 0, 12), enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit()

        pred_uc = results.get_forecast(steps=step)

        result[category] = pred_uc.predicted_mean.to_string()

    finished_time = dt.now().time().strftime("%H:%M:%S")

    task.result = json.dumps(result)
    task.status = "Success"
    task.started = started_time
    task.finished = finished_time
    db.session.commit()

    return render_template('predict.html', task=task)

@app.route('/result/<int:id>', methods = ['GET'])
def result_by_id(id):
    result = db.session.query(Task).filter(Task.id == id).first()
    if result:
        rbi = result
        return render_template('results.html', rbi=rbi)

    flash('Result not found.', 'danger')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)