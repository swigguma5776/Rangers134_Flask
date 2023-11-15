from flask import Blueprint, render_template, request, redirect, flash 
from werkzeug.security import check_password_hash 
from flask_login import login_user, logout_user 


#internal import 
from rangers_shop.models import User, db 
from rangers_shop.forms import RegisterForm, LoginForm



#instantiate our blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates') #template folder is navigating to where html files are located


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    #we need to instantiate our form as an object in order to use it
    registerform = RegisterForm()

    if request.method == 'POST' and registerform.validate_on_submit():
        #grabbing our data from our form after it was submitted 
        first_name = registerform.first_name.data 
        last_name = registerform.last_name.data 
        username = registerform.username.data 
        email = registerform.email.data 
        password = registerform.password.data 

        print(email, password, username)

        #query into database to check for username &/or email that already exists

        if User.query.filter(User.username == username).first():
            flash(f"Username already exists. Please Try Again", category='warning')
            return redirect('/signup')
        if User.query.filter(User.email == email).first():
            flash("Email already exists. Please Try Again", category='warning')
            return redirect('/signup')
        
        #we can now instantiate a new user object!!!
        
        user = User(username, email, password, first_name, last_name) 

        #now we can add our user object to our database
        db.session.add(user) #think of this like "git add ."
        db.session.commit() #think of this like "git commit"


        flash(f"You have successfully registered user {username}", category='success')
        return redirect('/signin')
    
    return render_template('sign_up.html', form=registerform )


@auth.route('/signin', methods=['GET', 'POST'])
def signin():

    #instantiate my loginform
    loginform = LoginForm()


    if request.method == 'POST' and loginform.validate_on_submit():
        #grab our data from the form
        email = loginform.email.data
        password = loginform.password.data 
        print("login info", email, password)

        user = User.query.filter(User.email == email).first()


        if user and check_password_hash(user.password, password): 
            #this is where we are using our UserMixin class & load_user() function
            login_user(user) #this is now saved as current_user everywhere in our application 
            flash(f"Successfully logged in {email}", category='success') 
            return redirect('/') #so if a user successfully logs in, we are going to send them home 
        else:
            flash("Invalid Email or Password, Please Try Again", category='warning')
            return redirect('/signin')
    
    return render_template('sign_in.html', form=loginform )


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')


    

