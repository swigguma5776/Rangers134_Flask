#this is our configuration folder to configure flask to our app location & variables needed to run Flask


import os #operating system 
from dotenv import load_dotenv #allows us to load our environment variables (variables needed to run application)


# establish our base directory so whenever we use "." to reference any location in our app it knows we are referncing
# rangers_shop folder 
basedir = os.path.abspath(os.path.dirname(__file__))


#need to establish where our environment variables are coming from (this file will be hidden from github)
load_dotenv(os.path.join(basedir, '.env'))



#create our Config class 
class Config():

    """
    Create Config class which will setup our configuration variables.
    Using Environment variables where available other create config variables. 
    """


    FLASK_APP = os.environ.get('FLASK_APP') #looking for key of FLASK_APP in our environment vaariable location (.env)
    FLASK_ENV = os.environ.get('FLASK_ENV') 
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Literally whatever you want as long as its a string. Cool Beans'
