from bottle import run, route, template, request, response, redirect, app
import os
from beaker.middleware import SessionMiddleware

#Einfalt cookie sýnidæmi
'''''
@route('/')
def index():
    if request.get_cookie('hello'):
        return 'Hello again'
    else:
        response.set_cookie('hello', 'world')
        return "cookies test"
'''''
#----------------------------
#Liður 1 cookies
adminuser = 'admin'
adminpwd = '12345'

@route('/')
def index():
    return template('index')

@route('/login')
def login():
    return template('login')

@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username == adminuser and password == adminpwd:
        response.set_cookie('account', username, secret='my_secret_code')
        return redirect('/restricted')
    else:
        return "Login failed. <br> <a href='login'>Login</a>"

@route('/restricted')
def restricted():
    user = request.get_cookie('account', secret='my_secret_code')
    if(user):
        return "Restriced area <br> " \
               "<a href='/signout'> Log off</a>"
    else:
        return "You are no logged in. Access denied."

@route('/signout')
def signput():
    response.set_cookie('account', "", expires=0)
    return "You have signed out" \
           "<br> <a href='/login'>Log in</a>"

#-------------------------------
#Liður 2 sessions

session_opts = {
    'session.type': 'file',
    'session.data_dir': './data'
}

my_session = SessionMiddleware(app(), session_opts)

products = [
    {"pid": 1, "name": "Vara A", "price": 100},
    {"pid": 2, "name": "Vara B", "price": 650},
    {"pid": 3, "name": "Vara C", "price": 200},
    {"pid": 4, "name": "Vara D", "price": 550}

]

@route('/shop')
def shop():
    return template('shop', products=products)

@route('/cart/add/<id>')
def add_to_cart(id):
    session = request.environ.get('beaker.session')
    session[id] = products[int(id)-1]['name']
    session.save()
    print(session)

    return redirect('/cart')

@route('/cart')
def cart():
    session = request.environ.get('beaker.session')
    karfa = []
    for i in range(1, len(products)+1):
        i = str(i)
        if session.get(i):
            vara = session.get(i)
            karfa.append(vara)
    return template('cart', karfa=karfa)

@route('/cart/remove')
def remove_cart():
    session = request.environ.get('beaker.session')
    session.delete()
    return redirect('/shop')

run(app=my_session,)