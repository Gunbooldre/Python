from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user
from flask import flash, request,render_template,redirect,url_for
from time import sleep

from application  import db ,app
from application.database import Login


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('rememberMe')
    if (remember =='on'):
        remember = True
    

    if username and password:
        user = Login.query.filter_by(username=username).first()
        # if login_user(user,remember=remember):
        #     return recept()
        print(remember)
        if user and check_password_hash(user.password, password):
            login_user(user,remember=True)
            print(remember)
            return recept()
        else:
            flash('Login or password is not correct',category='error')
    else:
        flash('Please fill login and password fields',category='error')

    return render_template('login.html')

@app.route('/regist/', methods=['post', 'get'])
def regist():
    if request.method == 'POST':
        if len(request.form['username']) != 0: 
            if len(request.form['password']) == len(request.form['password2']):
                if request.form['password'] == request.form['password2']:
                    hash = generate_password_hash(request.form['password'])
                    ses = Login(username=request.form['username'],password=hash)
                    if ses:
                        flash('Success registration',category='success')
                    db.session.add(ses)
                    db.session.commit()
                    sleep(3)
                    return redirect('/')
                else:
                    flash('Password not same',category='error')
                    db.session.rollback()

            else:
                    flash('Error, your password not correct',category='error')
                    db.session.rollback()
        else:
            flash('Your username is empty',category='error')
            db.session.rollback()
    return render_template('regist.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))



    

@app.route('/recept/')
def recept():
    return render_template('recept.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'),404

@app.route('/')
def index():
    return render_template('work.html')