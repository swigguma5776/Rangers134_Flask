from flask import Blueprint, flash, redirect, render_template, request


#internal import 
from rangers_shop.models import Product, Customer, Order, db 
from rangers_shop.forms import ProductForm



#need to instantiate our Blueprint class
site = Blueprint('site', __name__, template_folder='site_templates' )


#use site object to create our routes
@site.route('/')
def shop():

    #we need to query our database to grab all of our products to display
    allprods = Product.query.all() #the same as SELECT * FROM products, list of objects 
    allcustomers = Customer.query.all()
    allorders = Order.query.all()

    #making our dictionary for our shop stats/info

    shop_stats = {
        'products' : len(allprods), #this is how many total products we have
        'sales' : sum([order.order_total for order in allorders]),  #[ 27.99, 83.25, 50.99 ] sum them bad boys up
        'customers' : len(allcustomers)
    }


    our_class = "Rangers are the best "
                            #whats on left side is html, right side is whats in our route
    return render_template('shop.html', shop=allprods, coolmessage = our_class, stats=shop_stats ) #looking inside our template_folder (site_templates) to find our shop.html file


@site.route('/shop/create', methods= ['GET', 'POST'])
def create():

    #instantiate our productform

    createform = ProductForm()

    if request.method == 'POST' and createform.validate_on_submit():
        #grab our data from our form
        name = createform.name.data
        image = createform.image.data
        description = createform.description.data
        price = createform.price.data
        quantity = createform.quantity.data 

        #instantiate that class as an object passing in our arguments to replace our parameters 
        
        product = Product(name, price, quantity, image, description)

        db.session.add(product) #adding our new instantiating object to our database
        db.session.commit()

        flash(f"You have successfully created product {name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/shop/create')
    

    return render_template('create.html', form=createform )


@site.route('/shop/update/<id>', methods=['GET', 'POST']) #<parameter> this is how pass parameters to our routes 
def update(id):

    #lets grab our specific product we want to update
    product = Product.query.get(id) #this should only ever bring back 1 item/object
    updateform = ProductForm()

    if request.method == 'POST' and updateform.validate_on_submit():

        product.name = updateform.name.data 
        product.image = updateform.image.data 
        product.description = updateform.description.data 
        product.price = updateform.price.data 
        product.quantity = updateform.quantity.data 

        #commit our changes
        db.session.commit()

        flash(f"You have successfully updated product {product.name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/')
    
    return render_template('update.html', form=updateform, product=product )


@site.route('/shop/delete/<id>')
def delete(id):

    #query our database to find that object we want to delete
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect('/')