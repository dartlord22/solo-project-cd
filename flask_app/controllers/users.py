from flask_app import app 
from flask_app.models.user import User
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return redirect('/user/login')

@app.route('/user/login')
def login():
    return render_template('login.html')

@app.route('/user/register')
def register():
    return render_template('registration.html')

@app.route('/user/login/process', methods=['POST'])
def login_success():
    valid_user = User.validate_login(request.form)
    if not valid_user:
        return redirect('/user/login')
    
    user = User.get_by_email(request.form)
    session['user_id'] = user.id    
    
    return redirect('/events')

@app.route('/user/register/process', methods=['POST'])
def register_success(): 
    if not User.validate_registration(request.form):
        return redirect('/user/register')
    data ={ 
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.save(data)
    
    user = User.get_by_email(request.form)
    session['user_id'] = user.id 
    
    return redirect('/user/login')

@app.route('/user/profile')
def my_profile():
    return render_template('my_profile.html', user=User.get_user_info({'id':session['user_id']}))

@app.route('/user/profile/save', methods=['POST'])
def my_profile_submit():
    data={
        'profile_picture': request.form['profile_picture']
    }
    User.save_picture(data)
    return redirect('my_profile.html')

@app.route('/logout')
def logout():
    return redirect('/')

