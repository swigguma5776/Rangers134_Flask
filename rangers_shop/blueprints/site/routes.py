from flask import Blueprint, render_template 



#need to instantiate our Blueprint class
site = Blueprint('site', __name__, template_folder='site_templates' )


#use site object to create our routes
@site.route('/')
def shop():
    return render_template('shop.html') #looking inside our template_folder (site_templates) to find our shop.html file