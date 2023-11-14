from flask import Flask 
from .blueprints.site.routes import site 

#instantiating our Flask app
app = Flask(__name__) #passing in the __name__ variable which just takes the name of the folder we're in


#we are going to use a decorator to create our first route
# @app.route("/")
# def hello_world():
#     return "<p>Hello World!</p>"


app.register_blueprint(site)


